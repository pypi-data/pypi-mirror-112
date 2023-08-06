import base64

import praw

from .utils import resolveModelFromInput, resolveUser
from ..mixins import BaseApp
from praw.util.token_manager import BaseTokenManager

import logging

log = logging.getLogger(__package__)


class RedditApp(BaseApp):
    """A class for Reddit Apps.

    To obtain an instance of this class execute:

    .. code-block:: python

        bot = credmgr.bot("BotName")
        redditApp = bot.redditApp

    """

    _attrTypes = {
        **BaseApp._attrTypes,
        "client_id": "str",
        "client_secret": "str",
        "app_description": "str",
        "user_agent": "str",
        "app_type": "str",
        "redirect_uri": "str",
        "state": "str",
    }

    _editableAttrs = BaseApp._editableAttrs + [
        "clientId",
        "clientSecret",
        "appDescription",
        "userAgent",
        "appType",
        "redirectUri",
    ]
    _path = "/reddit_apps"
    _credmgrCallable = "redditApp"
    _reddit = None

    def __init__(self, credmgr, **kwargs):
        """Initialize a Reddit App instance.

        Reddit Apps are used for interacting with reddit

        :param credmgr: An instance of :class:`.CredentialManager`.
        :param int id: ID of this Reddit App.
        :param str name: Name of this Reddit App.
        :param str clientId: Client ID of this Reddit App.
        :param str clientSecret: Client secret of the Reddit App.
        :param str appDescription: Description of what this Reddit App is used for.
        :param str userAgent: The user agent used to identify this Reddit App to Reddit.
        :param str appType: Type of app this Reddit App is. One of: ``web``,
            ``installed``, or ``script``.
        :param str redirectUri: URL that redditors are redirected to after authorizing
            this Reddit App to access their account.
        :param str state: Used to identify this Reddit App during the OAuth2 flow.
        :param int ownerId: ID of the `.User` that owns this Reddit App.

        """
        super().__init__(credmgr, **kwargs)

        if "state" in kwargs:
            self._fetched = True

    @staticmethod
    @resolveUser()
    def _create(
        _credmgr,
        name,
        clientId,
        userAgent,
        appType,
        redirectUri,
        clientSecret,
        appDescription,
        enabled,
        owner=None,
    ):
        """Create a new Reddit App

        Reddit Apps are used for interacting with Reddit

        :param str name: (required)
        :param str clientId: Client ID of the Reddit App (required)
        :param str userAgent: User agent used for requests to Reddit's API (required)
        :param str appType: Type of the app. One of `web`, `installed`, or `script`
            (required)
        :param str redirectUri: Redirect URI for Oauth2 flow. Defaults to user set
            redirect uri (required)
        :param str clientSecret: Client secret of the Reddit App
        :param str appDescription: Description of the Reddit App
        :param bool enabled: Allows the app to be used (defaults to `True`)
        :param Union[User,int,str] owner: Owner of the bot. Requires Admin to create for
            other users.

        :returns: RedditApp

        """
        data = {
            "app_name": name,
            "client_id": clientId,
            "user_agent": userAgent,
            "app_type": appType,
            "redirect_uri": redirectUri,
        }
        if clientSecret:
            data["client_secret"] = clientSecret
        if appDescription:
            data["app_description"] = appDescription
        if enabled:
            data["enabled"] = enabled
        if owner:
            data["owner_id"] = owner
        return _credmgr.post("/reddit_apps", data=data)

    def reddit(self, redditor=None, reddit=praw.Reddit) -> praw.Reddit:
        """Provides an optionally authenticated [Async] PRAW

        :param str redditor: The redditor that you want the Reddit instance authorized
            as.
        :param reddit: The Reddit class to use. Useful if you have a local version of
            PRAW.

        :returns: Reddit instance.

        """
        if not self._reddit:
            extra_kwargs = {}
            if redditor:
                extra_kwargs["token_manager"] = RefreshTokenManager(
                    self._credmgr, redditor, self
                )
            self._reddit = reddit(
                client_id=self.clientId,
                client_secret=self.clientSecret,
                user_agent=self.userAgent,
                redirect_uri=self.redirectUri,
                **extra_kwargs,
            )
        return self._reddit

    def genAuthUrl(self, scopes=None, permanent=False, userVerification=None):
        """Generates a URL for users to verify or authenticate their Reddit account

        :param Union[list,str] scopes: List of scopes needed. Pass ``'all'`` for all
            scopes. The ``identity`` scope will always be included. (default:
            ``['identity']``)
        :param bool permanent: Determines if a refresh token will be provided. (default:
            ``False``)
        :param Union[UserVerification,int,str] userVerification: Link to a
                :class:`.UserVerification`
                object. Accepted values are:

                - An :class:`.UserVerification` object
                - An :class:`.UserVerification` ``id``
                - An ``userId`` of a :class:`.UserVerification` record.

            If a :class:`.UserVerification` record does not exist, one will be created.

        :returns: Auth URL

        """
        from credmgr.models import UserVerification

        if scopes is None or scopes == "identity":
            scopes = ["identity"]
        elif scopes == "all":
            scopes = ["*"]
        if "identity" not in scopes and scopes != ["*"]:
            scopes = [scopes, "identity"]
        if permanent:
            duration = "permanent"
        else:
            duration = "temporary"
        uVerification = resolveModelFromInput(
            self._credmgr, UserVerification, userVerification, "userId"
        )
        if not uVerification and userVerification:
            uVerification = self._credmgr.userVerification.create(
                userVerification, self.id
            )
        if uVerification:
            state = base64.urlsafe_b64encode(
                f"{self.state}:{uVerification}".encode()
            ).decode()
        else:
            state = self.state
        return self.reddit().auth.url(scopes, state, duration)


class RefreshTokenManager(BaseTokenManager):
    def __init__(self, credmgr, redditor, reddit_app):
        self._credmgr = credmgr
        self.redditor = redditor
        self.reddit_app = reddit_app
        self.refreshToken = self._credmgr.refreshToken(
            self.redditor, self.reddit_app.id
        )
        super().__init__()

    def post_refresh_callback(self, authorizer):
        log.debug(
            f"Storing new refresh token for app: {self.reddit_app.name}({self.reddit_app.id}) redditor: u/{self.redditor}"
        )
        self.refreshToken.edit(refreshToken=authorizer.refresh_token)
        log.debug(
            f"Successfully sorted new refresh token for app: {self.reddit_app.name}({self.reddit_app.id}) redditor: u/{self.redditor}"
        )

    def pre_refresh_callback(self, authorizer):
        log.debug(
            f"Fetching refresh token for app: {self.reddit_app.name}({self.reddit_app.id}) redditor: u/{self.redditor}"
        )
        refreshToken = self._credmgr.refreshToken(self.redditor, self.reddit_app.id)
        log.debug(
            f"Fetched refresh token for app: {self.reddit_app.name}({self.reddit_app.id}) redditor: u/{self.redditor}"
        )
        if refreshToken:
            authorizer.refresh_token = refreshToken.refreshToken
