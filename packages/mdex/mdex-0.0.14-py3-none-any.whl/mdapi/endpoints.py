class Endpoints:
    COVERS = "https://uploads.mangadex.org/covers/{}/{}"

    class Manga:
        SEARCH = ("GET", "/manga")
        CREATE = ("POST", "/manga")
        TAGS = ("GET", "/manga/tag")
        BATCH_GET_READ = ("GET", "/manga/read")
        RANDOM = ("GET", "/manga/random")
        GET = ("GET", "/manga/{manga}")
        EDIT = ("PUT", "/manga/{manga}")
        DELETE = ("DELETE", "/manga/{manga}")

        SET_STATUS = ("POST", "/manga/{manga}/status")

        FOLLOW = ("POST", "/manga/{manga}/follow")
        UNFOLLOW = ("DELETE", "/manga/{manga}/follow")

        CHAPTERS = ("GET", "/manga/{manga}/feed")
        MARK_READ = ("GET", "/manga/{manga}/read")

        ADD_TO_LIST = ("POST", "/manga/{manga}/list/{list}")
        REMOVE_FROM_LIST = ("DELETE", "/manga/{manga}/list/{list}")

    class Cover:
        SEARCH = ("GET", "/cover")
        UPLOAD = ("POST", "/cover/{manga}")
        EDIT = ("PUT", "/cover/{cover}")
        DELETE = ("DELETE", "/cover/{cover}")

    class Auth:
        LOGIN = ("POST", "/auth/login")
        CHECK = ("GET", "/auth/check")
        LOGOUT = ("POST", "/auth/logout")
        REFRESH = ("POST", "/auth/refresh")

    class Account:
        CREATE = ("POST", "/account/create")
        RECOVER = ("POST", "/account/recover")
        COMPLETE_RECOVER = ("POST", "/account/recover/{code}")
        ACTIVATE = ("GET", "/account/activate/{code}")
        ACTIVATE_RESEND = ("POST", "/account/activate/resend")

    class Group:
        SEARCH = ("GET", "/group")
        CREATE = ("POST", "/group")
        GET = ("GET", "/group/{group}")
        EDIT = ("PUT", "/group/{group}")
        DELETE = ("DELETE", "/group/{group}")
        FOLLOW = ("POST", "/group/{group}/follow")
        UNFOLLOW = ("DELETE", "/group/{group}/follow")

    class List:
        CREATE = ("POST", "/list")
        GET = ("GET", "/list/{list}")
        EDIT = ("PUT", "/list/{list}")
        DELETE = ("DELETE", "/list/{list}")
        GET_FEED = ("GET", "/list/{list}/feed")

    class User:
        GET_ME = ("GET", "/user/me")
        LIST = ("GET", "/user/list")
        OTHER_LIST = ("GET", "/user/{user}/list")
        FOLLOWS_GROUP = ("GET", "/user/follows/group")
        FOLLOWS_MANGA = ("GET", "/user/follows/manga")
        FOLLOWS_CHAPTERS = ("GET", "/user/follows/manga/feed")

    class Chapter:
        SEARCH = ("GET", "/chapter")
        GET = ("GET", "/chapter/{chapter}")
        EDIT = ("PUT", "/chapter/{chapter}")
        DELETE = ("DELETE", "/chapter/{chapter}")
        MARK_READ = ("POST", "/chapter/{chapter}/read")
        MARK_UNREAD = ("DELETE", "/chapter/{chapter}/read")

    class Author:
        CREATE = ("POST", "/author")
        SEARCH = ("GET", "/author")
        GET = ("GET", "/author/{author}")
        EDIT = ("PUT", "/author/{author}")
        DELETE = ("DELETE", "/author/{author}")

    class Upload:
        GET_SESSION = ("GET", "/upload")
        BEGIN = ("GET", "/upload/begin")
        ADD_IMAGE = ("POST", "/upload/{session}")
        DELETE_IMAGE = ("DELETE", "/upload/{session}/{file}")
        ABADON = ("DELETE", "/upload/{session}")
        COMMIT = ("POST", "/upload/{session}/commit")

    GET_MD_AT_HOME = ("GET", "/at-home/server/{chapter}")
    SOLVE_CAPTCHA = ("POST", "/captcha/solve")
    LEGACY_MAPPING = ("POST", "/legacy/mapping")

    MDAH_REPORT = ("POST", "https://api.mangadex.network/report")
