# Bing Wallpaper for macOS

一个极简的 macOS 必应壁纸更新工具：在桌面双击一下 **更新壁纸.app**，
当天的 Bing 主页大图就会被设为桌面壁纸。

- **零依赖**：使用系统自带的 `/usr/bin/python3` 与标准库（`urllib`、`json`、`hashlib`、`subprocess`），不需要 `pip install` 任何东西。
- **纯原生**：通过 `osascript` / AppleScript 设置壁纸（`tell every desktop to set picture to ...`）和发送通知。
- **不常驻**：没有任何后台进程、没有定时任务，只在你点按钮时跑一次。

## 文件说明

| 文件 | 作用 |
| --- | --- |
| [main.py](main.py) | 抓取 Bing 图片并设置为桌面壁纸（仅用 Python 标准库）。 |
| [RUNME.sh](RUNME.sh) | 读取 `config.yml`，用系统 Python 调用 `main.py`。 |
| [config.yml](config.yml) | 项目路径 `path` 和图片日期 `mode`。 |
| [picture/](picture) | 保存最近一次下载的壁纸 `background.jpg`。 |

## 一次性配置

1. 打开 [config.yml](config.yml)，把 `path` 改成本仓库在你电脑上的绝对路径：

   ```yaml
   path: /Users/yourname/Projects/BingWallpaper-Ubuntu
   mode: 0      # 0=今天, 1=昨天, 2-7=N 天前
   ```

2. 给脚本加执行权限（仅首次需要）：

   ```bash
   chmod +x RUNME.sh
   ```

3. 在桌面生成 **更新壁纸.app**：

   ```bash
   /usr/bin/osacompile -o "$HOME/Desktop/更新壁纸.app" \
       -e "do shell script \"/bin/bash '$PWD/RUNME.sh'\""
   ```

   这是一个原生 AppleScript 应用，双击即跑，不会弹出终端窗口。
   也可以拖到 Dock 或访达侧边栏当常驻按钮。

4. **首次运行会有两个授权弹窗**，都需要点「允许」：
   - 通知权限（用于显示「Wallpaper updated successfully」）
   - 自动化权限：允许控制「系统事件」（用于设置壁纸）

   如果不小心点了不允许，去：
   *系统设置 → 隐私与安全性 → 自动化* 中重新勾选 “系统事件”。

## 日常使用

想换今天的壁纸时，桌面双击 **更新壁纸.app** 即可。
不需要更新的日子完全无负担，没有任何后台活动。

也可以在终端里手动跑：

```bash
./RUNME.sh
```

## 更换图标 / 重命名

- **改图标**：右键 `更新壁纸.app` → 显示简介，把一张 `.png`/`.icns` 拖到左上角小图标上。
- **改名**：直接在桌面重命名即可，不影响功能。

## 移动仓库位置后

`.app` 里硬编码了脚本路径，所以仓库目录搬家后需要重新生成一次：

```bash
cd /新/路径/BingWallpaper-Ubuntu
/usr/bin/osacompile -o "$HOME/Desktop/更新壁纸.app" \
    -e "do shell script \"/bin/bash '$PWD/RUNME.sh'\""
```

并记得同步修改 [config.yml](config.yml) 里的 `path`。

## 常见问题

- **点了按钮没反应？** 在终端运行 `./RUNME.sh` 看真实报错；通常是首次未授予自动化 / 通知权限。
- **壁纸没变但通知说成功？** 因为今日图片与本地已有的 `picture/background.jpg` 一致（脚本会做 md5 比对避免重复写文件）。想强制刷新：`rm picture/background.jpg && ./RUNME.sh`。
- **想取回 Ubuntu 版本？** 切到 `main` 分支：`git checkout main`。
