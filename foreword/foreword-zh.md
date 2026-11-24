# MacWave / LinuxWave 使用手册

### Welcome to Wave World!

欢迎使用 MacWave/LinuxWave ！使用前建议你阅读下面的手册：

### 基本命令
`wave` 的基本命令你可能比较熟悉，为了让你更快了解，我们提供了你可能常用的参数命令组合：

| 组合 | 用途 | 何时用 | 备注 |
| --- | --- | --- | --- |
| `wave -h` | 查看帮助信息 | 不知道某个命令怎么用 | `wave -h --zh`可以输出中文版帮助 |
| `wave manual --color` | 输出彩色帮助 | 同上，不过更详细 | `wave manual --zh`可以输出中文版帮助 |
| `wave -V` | 查看MacWave的版本号 | 查看当前MacWave版本 | |
| `wave install <pkg_name>`  | 安装一个软件包 | 安装软件 | `wave install <pkg_name>@<pkg_version>` 可以安装指定版本的软件包 |
| `wave upgrade -X` | 升级一个软件包 | 一般的升级软件 | 适用于一般的开发者。 `-X, --remove-old-versions` 会删除存在的旧版软件包。请确认你不需要旧版，否则不要使用此参数 |
| `wave latest <pkg_name>` | 查看某个包有没有比本机更新的版本 | 不知道某个包能不能升级 | `wave latest -a` 可查看所有包的状态 |
| `wave selfupdate` | 更新MacWave自身 | 当你想升级你的MacWave | |
| `wave list` | 列举出已经安装的软件包和它们的版本号 | 想知道自己装了什么软件或什么版本的软件 | `wave list -a` 也是同样效果 |
| `wave info <pkg_name>` | 查看你安装了这个软件包的什么版本（未安装时输出 `None`） | 不知道自己是否安装过某个软件包、或不知道装过什么版本 | |
| `wave search <pkg_name>` | 搜索一个软件包（可输出部分内容然后模糊匹配）| 想要搜 `wave` 有没有这个包 | |
| `wave uninstall <pkg_name>` | 删除某个包 | 删除软件 |  `wave uninstall <pkg_name>@<pkg_version>` 可以删除指定版本的软件包 |

更多帮助，请运行 `wave -h`、`wave -h --zh`（中文版）或 `wave manual`、`wave manual --zh`（中文版）。

注：实际执行命令时，请把上述 `<占位符>` 换成实际内容。

### 安装位置

**注：下列只是我们推荐的目录，实际中你可以任意选择甚至自定义（推荐在前）：**

macOS（共享安装，推荐）：`/opt/macwave`  
macOS（单用户安装）： `~/.local/macwave`  
Linux（共享安装，推荐）：`/home/linuxwave/.linuxwave`  
Linux（单用户安装）： `~/.local/linuxwave`  

注意：在 Intel Mac 不建议选择 `/usr/local` —— 这可能和 Homebrew 在 Intel Mac 的默认目录冲突。

**配置文件存储于（系统级安装始终优先）：**  

**MacWave：**

1. `/opt/macwave_config`        共享安装
2. `~/.config/macwave_config`   单用户安装

**LinuxWave：**

1. `/etc/linuxwave_config`      共享安装
2. `~/.config/linuxwave_config` 单用户安装

**警告：请不要随意修改配置文件 —— 这可能导致 `wave` 的某些行为异常或不符合预期！**

#### 每个目录的优缺点

选之前值得看一眼：权限模型、依赖占多少磁盘、以后搬不搬得走都不一样。

**macOS（MacWave）**

| 目录 | 适合谁 | 优点 | 缺点 |
| --- | --- | --- | --- |
| **`/opt/macwave`（推荐，默认）** | 自己就是管理员、这台机器只装一份 | 依赖只有**一份**，多用户共用（`deps/` 常常几百 MB）；树是 `root:<管理员组>` 775（目录 setgid），管理员组成员**装包不用 sudo**；与 Homebrew（`/opt/homebrew`）同一套心智；不受 `$HOME` 影响，搬机、改用户名、用 `sudo` 跑脚本都不会打偏 | 安装时要**一次**管理员密码；树是共享状态，同机多个管理员会互相影响（这也正是「依赖只有一份」的另一面）；卸载要动 root 名下的文件（目录组可写，通常不需要额外 sudo） |
| `~/.local/macwave` | 拿不到管理员密码、只想给自己装、想随手删 | 全程**不需要 sudo**；完全属于你，`rm -rf` 就没了；不写系统目录 | 依赖不共享：每个用户各一份；`$HOME` 一变（换用户名、搬机、`sudo` 下跑）就可能找不到；`PATH` 要跟 `$HOME` 走 |
| `/usr/local/macwave` | Intel Mac 上习惯 `/usr/local` 的人 | 共享模型与 `/opt` 相同（775 setgid） | **Intel 上可能和 Homebrew 冲突**（Homebrew 的默认前缀就是 `/usr/local`）；Apple 芯片上 `/usr/local` 又不是 Homebrew 的位置，容易两套东西混放 |
| 自定义路径 | 外置卷、想同时装多份 | 完全自由 | 共享/权限模型要自己定；别忘了把 `<目录>/bin`、`<目录>/links`、`<目录>/lib` 加进 `PATH` |

不想记的话：`wave basedir --raw` 会打印当前装在哪，`wave basedir --set <新目录>` 能把整棵树
搬走（要求先跑 `wave transfer --all`，让产物变成位置无关的）。

**Linux（LinuxWave）**

| 目录 | 适合谁 | 优点 | 缺点 |
| --- | --- | --- | --- |
| **共享安装（`/home/linuxwave/.linuxwave`，推荐）** | 多用户机器、或要跑服务 | 依赖**只存一份**；树归专用账户 `linuxwave` 与**同名组**，组成员装包**不用 sudo**；配置在 `/etc/linuxwave_config`（`root:linuxwave` 2775）；整棵树可以跑在低权限账户下，守护进程不必是 root | 安装时要一次 sudo 来建账户/组与写 `/etc`；**装完必须重登录**（组身份在新会话才生效）或 `newgrp linuxwave`；组员能改整棵树，包括 `lib/wave` 本体 —— 等于把「谁能影响这台机器上的 MacWave/LinuxWave」限定在组内 |
| `~/.local/linuxwave` | 单用户、不想碰系统目录 | 不需要 sudo；随时删 | 依赖不共享；多用户机器上每人一份 |
| `/opt/linuxwave` | 单用户，但想要固定路径 | 装一次 sudo、之后归**你**（树与配置都属安装者）；路径固定、不受 `$HOME` 影响 | **不是真共享**：别的用户只能读、不能装包；发行版包管理器不认识它（升级/清理靠 `wave` 自己） |
| `/usr/local/linuxwave` | 习惯 FHS 的人 | 与 `/opt` 相同的「归安装者」模型 | 容易和手工 `make install` 的东西混在一起；排查「这份 `.so` 是谁装的」会变难 |

> 给共享安装加人：`sudo usermod -aG linuxwave <user>`，然后让对方**重登录**。
> 只想给某个服务用：让服务以 `linuxwave` 账户运行，它天然拥有那个组。

### 镜像

如果你是中国大陆用户，你很可能还需要镜像。如果你使用的是全量镜像，需要在 `~/.zshrc` （若用 `bash` 则是 `~/.bashrc` ）添加的环境变量如下（一些好的镜像可能会引导你去执行命令添加）：

| 变量 | 取什么 | 默认 |
| --- | --- | --- |
| `MACWAVE_BOTTLE_DOMAIN` | 预编译软件包 | GitHub Releases |
| `MACWAVE_DEPS_DOMAIN` | 依赖库 | GitHub Releases |
| `MACWAVE_API_DOMAIN` | 软件包索引 | raw.githubusercontent 上的 `infosource` |
| `MACWAVE_SELFUPDATE_DOMAIN` | 自更新数据 | raw.githubusercontent 上的 `Selfupdate` |
| `MACWAVE_PYTHON_DOMAIN` | 自带解释器 | raw.githubusercontent 上的 `Python` |
| `MACWAVE_CORE_DOMAIN` | MacWave 自身文件 | raw.githubusercontent 上的 `MacWave` |
| `MACWAVE_PIP_INDEX` | `pip` 的索引（只影响三个 Python 依赖） | `https://pypi.org/simple` |

**`infosource` 后面的 ref 段不能少：** MacWave 是 `/HEAD`，LinuxWave 是 `/main`
（镜像按 `<组织>/<仓库>/<ref>/…` 布局）。少了这一段，`wave search`、`wave latest`
读清单时只会得到 404。

执行下面的命令即可添加：

```zsh
export MACWAVE_BOTTLE_DOMAIN=https://mirror.example.cn/MacWave/bottle
export MACWAVE_DEPS_DOMAIN=https://mirror.example.cn/MacWave/deps
export MACWAVE_API_DOMAIN=https://mirror.example.cn/MacWave/infosource/HEAD
export MACWAVE_SELFUPDATE_DOMAIN=https://mirror.example.cn/MacWave/selfupdate
export MACWAVE_PYTHON_DOMAIN=https://mirror.example.cn/MacWave/python
export MACWAVE_CORE_DOMAIN=https://mirror.example.cn/MacWave/core
export MACWAVE_PIP_INDEX=https://pypi.mirror.example.cn/simple
```

`export` 只在当前终端有效，关掉就没了。把这个块追加进 `~/.zshrc`，此后每个终端自动继承。追加命令如下：

```zsh
cat >> ~/.zshrc <<'MWMIRROR'

# MacWave mirror
export MACWAVE_BOTTLE_DOMAIN=https://mirror.example.cn/MacWave/bottle
export MACWAVE_DEPS_DOMAIN=https://mirror.example.cn/MacWave/deps
export MACWAVE_API_DOMAIN=https://mirror.example.cn/MacWave/infosource/HEAD
export MACWAVE_SELFUPDATE_DOMAIN=https://mirror.example.cn/MacWave/selfupdate
export MACWAVE_PYTHON_DOMAIN=https://mirror.example.cn/MacWave/python
export MACWAVE_CORE_DOMAIN=https://mirror.example.cn/MacWave/core
export MACWAVE_PIP_INDEX=https://pypi.mirror.example.cn/simple
MWMIRROR
source ~/.zshrc
```
其中 `MACWAVE_PIP_INDEX` 只影响 `pip` 安装的三个 Python 依赖（`requests`、`toml`、`colorama`），所以可以指向任意 PyPI 镜像（国内推荐的有：UTSC（中科大）、TUNA（清华）等）。  

运行一次即可。新开的终端自己会读到，末尾的 `source` 只是让当前终端立刻生效。用不上的行可以删掉 —— 少写几行也能用，没设的变量会回落到官方地址。
  
如果以后不想用镜像了，把他们删掉或注释掉即可。

LinuxWave 同理，只需要把上面的 `MACWAVE` 改为 `LINUXWAVE` 即可。注意 Linux 默认的是 `bash` 。

### 联系方式

若有问题，可在项目 GitHub 提 issue 或给 `macwaveorg@outlook.com` 写信来联系我们。

**祝你（waver）有愉快的冲浪（surf）体验！**

