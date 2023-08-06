这是一个获取电影链接的工具
================
获取美剧天堂（https://www.meijutt.tv/）中的指定页面中的链接
-----------
例子：
```
import MovieHelper.MovieLink
url="https://www.meijutt.tv/content/meiju26535.html";
mylist = MovieHelper.MovieLink.GetMovieLink(url)
for item in mylist:
     print(item)
```