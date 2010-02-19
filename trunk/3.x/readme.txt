博文批量发布工具


用Python写的离线批量发布博客文章的工具，又称pyBlogPost，
支持一次上传到多个服务器；
支持只向一个指定的服务器上传图片，其它地方直接应用；
支持检查文件/图片是否有更新，只上传更新的文件/图片，避免每次更新文章都向服务器上传所有图片。

功能列表
===================
1、支持向WordPress空间发布带图的文章。
2、支持一次向多个服务器发布文章。
3、支持通过xml文件配置服务器参数。
4、支持发布WizKnowedge文章。
5、支持指定一个博客服务器上传图片，其它博客直接链接。
6、支持每个博客都单独上传图片。
7、文章有修改的时候，只更新已发布的文章。
8、文章无修改的时候，不更新也不发布文章。
9、图片也是在有修改的时候，才重新上传，不会每次更新文章都把所有图片再上传一次。
10、通过此工具上传的文件固定连接地址可以在WordPress插件slug的作用下自动改为易于识别的英文或者拼音，而不是数字。（WK自带的上传无此功能）
11、根据MD5码是否相同判断文件是否有修改。
12、html文件没修改，只修改图片，那么图片不会单独上传。
13、可以修改MIME.xml以支持更多媒体文件类型。
14、支持作为WizKnowedge插件，并且在第一次发布时分配UUID，然后作为该文章的永久唯一标示。


使用方法
===================
需要先安装Python 3.1以上版本，并且把Python.exe所在目录添加到path变量中。
1、修改配置文件blogconfig.xml，配置为自己的博客服务器、账户参数。
2、运行命令：python.exe blogpost.py html_file file_guid [config_file data_file] (中括号内是可选参数)
3、最好的使用方法是作为WizKnowedge插件使用，那么需要在%USERPROFILE%\My Documents\My Knowledge\Plugins目录创建新的目录“{A0D025CD-970A-4C62-97E4-5CF6F2C9DD6A}”，
然后把代码库中“https://pyblogpost.googlecode.com/hg/trunk/3.x"所有代码下载到该目录。重新打开WizKnowedge，就可以看到插件菜单中多了一个”博文批量发布“。
注意需要先修改blogconfig.xml中的服务器配置，再发布文章。

说明：
1、file_guid是html文件的唯一身份识别码，无论文章怎么修改都保持不变，也不会与别的文章重复。guid输入0时，工具会自动生成一个，并且保存在工具目录下的lastpost_guid.ini。
2、为了能找到图片路径，如果发布文件为html，那么运行工具时的当前目录应该是html_file所在目录，特别是在html文件中以相对路径引用图片的情况下。
   如果发布的是ziw，则程序会自动解压缩到临时目录并且把当前目录切换到该临时目录。


配置文件
===================
默认文件名：blogconfig.xml
配置要发布到的博客服务器的相关信息。
注意：
1、posturl要指定为xmlrpc.php、metablogapi.aspx、RPC.ashx的完整路径，并且要是自己的博客账户的路径。
2、用户名、密码是你的博客账户的用户名、密码。（live space除外，参见后面说明）
内容格式如下：
<?xml version="1.0"?>
<config>
    <fileserver>  --- 指定的上传图片文件的服务器为fileserver
        <name>blog.sinojelly.dreamhosters.com</name>
        <system>wordpress</system>
        <posturl>http://blog.sinojelly.dreamhosters.com/xmlrpc.php</posturl>
        <username>admin</username>
        <password>123456</password>
        <postblog>true</postblog>   --- 是否发布文章到此blog, 不发布文章也就不会上传图片，【文件服务器必须设置为true】
        <media>2</media>   --- 【fileserver 必定为2】，否则失去意义
    </fileserver>
    <blog>  --- 可以有多个<blog>节点，从而向多个博客发布日志
        <name>sinojelly.20x.cc</name>
        <system>wordpress</system>
        <posturl>http://sinojelly.20x.cc/xmlrpc.php</posturl>
        <username>admin</username>
        <password>654321</password>
        <postblog>true</postblog>
        <media>0</media>  --- 是否向此服务器上传图片等媒体文件(0--不上传, 1--上传但远程路径只用于本博客，2--上传，远程路径用于后面所有博客)
    </blog>
</config>


数据文件
===================
默认文件名：blogdata.xml
发布文章后会自动生成此文件，请勿手动编辑。（发布文章很多，它变得太大，影响了效率，可以把它删除或者重命名）
<data>
    <html_file wk_file_guid="">
        <media>
            <file local_path="">
                <remote_path></remote_path>
                <file_hash></file_hash>
            </file>
        </media>
        <blog name="">
            <postid></postid>
            <file_hash></file_hash>  -- post file modify time
        </blog>
    </html_file>
<data>


LiveSpace
===================
为了使用MetaWeblog API编辑Live space空间中的博文内容，首先需要在空间启用E-mail发布功能，并设置密码字。

到你的空间中的Options->E-mail Publishing选项进行配置
打开E-mail发布功能，并选择 secred word的密码字。
在程序中会用到用户名和密码，如果你的空间地址为： oldname.spaces.live.com，则用户名就是oldname,而不是你的live id，密码则是上面设置的secred word,而不是live id的密码。


可改进点
===================
1、支持除WordPress以外的博客服务器。（架构支持很方便的扩展）
2、支持文章分类、标签。并且可以在指定某个博客固定使用的标签。
3、少数时候会遇到图片上传失败，上传同样图片WizKnowedge自带插件也会失败。
4、html文件解析是采用的正则表达式方式，可以考虑用lxml.html来解析，初步看一下似乎没有直接提供获得media列表的接口。（不过必要性不大，改进后的正则表达式少了很多.*，效率很高）


开源项目路径：
http://code.google.com/p/pyblogpost/

讨论组：
http://space.cnblogs.com/group/101223/

联系作者：
QQ: 2578717
MSN: sinojelly@msn.cn
email: sinojelly@163.com
新浪微博：http://t.sina.com.cn/sinojelly
我的博客：http://sinojelly.20x.cc
          http://sinojelly.blog.51cto.com/
          http://www.cnblogs.com/sinojelly/
简短附言：
欢迎各位朋友使用此工具，欢迎有兴趣的朋友继续完善它，或者提出改进意见，谢谢！
2010.2.13（大年三十） - 2010.2.19，春节期间，每天11：00-4：00，没别的成绩，就写了这个工具。
起初，只是想做个WizKnowedge插件扩展博客工具的功能，从对这个领域很陌生开始查找资料，最后选择Python来实现了它。
涉及与服务器的交付，不容易试验成功，后来终于向WordPress发布文章成功，然后实现了一个面向过程的简陋可用的版本。
后来发现它很难支持只发布新图片等功能，于是采用面向对象重写，研究了Python的xml操作等很多方面的内容，现学现用。
终于到现在，有了一个基本满足要求的版本。
遗憾的是暂时无法支持其它类型的博客，Python的xmlrpc库存在缺陷无法支持，需要自己实现；并且Python 3还不能支持https。


