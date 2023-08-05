# -*- coding: utf-8 -*-
"""
Copyright (c) 2015-2021 Stduino.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file or search www.stduino.com.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

from function.conf import res

from function.language import zh_hans as reso
try:

    if res.msg == "1":  # 中
        from function.language import zh_hans as reso

        pass
    elif res.msg == "2":  # 英
        from function.language import en as reso

        pass
    elif res.msg == "python3":  # 俄
        from function.language import russian as reso

        pass
    elif res.msg == "4":  # 德
        from function.language import german as reso

        pass
    elif res.msg == "5":  # 日
        from function.language import japanese as reso

        pass
    elif res.msg == "6":  # 韩
        from function.language import korean as reso

        pass
    elif res.msg == "7":  # 西班牙
        from function.language import spanish as reso

        pass
    elif res.msg == "8":  # 法
        from function.language import french as reso

        pass
    elif res.msg == "9":  # 阿拉伯语
        from function.language import arabic as reso

        pass
    else:  # 英
        from function.language import en as reso

        pass

except:
    print("language")
