## 就是個簡單的 Wrap

需要二個環境變數
- AUTH_URL

用來指定公司統一登入的 api 網址
- PMB_API_URL

用來指定 pmb 服務的網址

### 使用範例

```python
import os
import pmb_py as pmb
from pmb_py import log_in, log_out

log_in(YOUR_USERNAME, YOUR_PASSWORD)

projects = pmb.api.PmbProjects.list()
print(projects)

project = pmb.api.PmbProjects.get(id=100)
print(project)

log_out()
```