# pytrac

#关于

pytrac是一个用来写Trac的工具.

#使用方法

在config.py中配置好用户名、密码、Trac地址

    import config
    from pytrac import pytrac

    if __name__ == "__main__":

        trac_url = config.TRAC_URL
        user = config.TRAC_USER
        password = config.TRAC_PASS
        t = Trac(trac_url, user, password)
        path = 'wiki/work/solos/2014/3/7'
        content = '''
        {{{
        #!rst

            2014/3/7 日报
            ===============

            pytrac
            ------

            - add create function for pytrac.
            - add config.py.sample file

        }}}'''
        t.create(path, content)
