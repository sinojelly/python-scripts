@rem Modify the paths, and run this file, then the files in dist directory is distribution files.

if not exist dist mkdir dist

copy BatchPublishBlog.htm dist\BatchPublishBlog.htm
copy blogconfig.xml dist\blogconfig.xml
copy MIME.xml dist\MIME.xml
copy plugin.ini dist\plugin.ini
copy readme.txt dist\readme.txt

C:\Python31\Scripts\cxfreeze.bat   --include-path=C:\Python31\Lib\site-packages\lxml --init-script=D:\Projects\Google\pyblogpost\pyblogpost\trunk\3.x\BlogPost.py  BlogPost.py

@rem I found that when cxfreeze run finished, it closes the console window. pause is no use.

pause
