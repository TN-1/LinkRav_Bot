#!/usr/bin/python
# constant declarations

RAV = "ravelry.com/"
RAV_PERM = "http://www.ravelry.com/"
RAV_MATCH = "((?:http://)?(?:www\.)?ravelry\.com/[-|/|a-z|0-9]+|ravel\.me/[-|/|a-z|0-9]+)"
PAT_MATCH = "patterns/library/"
PROJ_MATCH = "projects/"
YARN_MATCH = "yarns/library/"

PAT_MATCH_LEN = len(PAT_MATCH)
PROJ_MATCH_LEN = len(PROJ_MATCH)
YARN_MATCH_LEN = len(YARN_MATCH)

PAT_REGEX = "(?<=" + RAV + PAT_MATCH + ")[^/]+"
PROJ_REGEX = "(?<=" + RAV + PROJ_MATCH + ")[^/]+/[^/]+"
YARN_REGEX = "(?<=" + RAV + YARN_MATCH + ")[^/]+"

PEOPLE_MATCH = "people/"
DESIGNER_MATCH = "designers/"
COMPANY_MATCH = "yarns/brands/"

RAV_API = "https://api.ravelry.com/"
PAT_API = RAV_API + "patterns/{}.json"
PROJ_API = RAV_API + "projects/{}.json"
YARN_API = RAV_API + "yarns/{}.json"

START_NOTE = "#####&#009;\n######&#009;\n####&#009;\n"
END_NOTE_I = "*To call me, put \"/u/RavBot\" in your post! | [About Me](https://github.com/TN-1/LinkRav_Bot/wiki) | [Contact Maintainer](https://www.reddit.com/message/compose/?to=randomstonerfromaus)*"
END_NOTE_S = "*I found this post by myself! [Opt-Out](https://goo.gl/forms/IYxecqcOhih3SS3F3) | [About Me](https://github.com/TN-1/LinkRav_Bot/wiki) | [Contact Maintainer](https://www.reddit.com/message/compose/?to=randomstonerfromaus)*"
