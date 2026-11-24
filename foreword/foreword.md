# MacWave / LinuxWave Handbook

### Welcome to Wave World!

Welcome to MacWave / LinuxWave! Before you start, we suggest reading the manual below.

### Basic commands

You are probably already familiar with the basic `wave` commands. To get you up to speed
faster, here are the flag-and-command combinations you are most likely to use:

| Combination | What it does | When to use it | Notes |
| --- | --- | --- | --- |
| `wave -h` | Print help | You are not sure how a command works | `wave -h --zh` prints the Chinese help |
| `wave manual --color` | Print the full manual in colour | Same, but more detail | `wave manual --zh` prints the Chinese manual |
| `wave -V` | Print the MacWave version | Checking which version you are on | |
| `wave install <pkg_name>` | Install a package | Installing software | `wave install <pkg_name>@<pkg_version>` installs one specific version |
| `wave upgrade -X` | Upgrade a package | Everyday upgrades | Aimed at regular users. `-X, --remove-old-versions` deletes the old copies — make sure you do not need them before using it |
| `wave latest <pkg_name>` | Check whether a newer version exists than the one you have | Wondering if a package can be upgraded | `wave latest -a` shows the status of every package |
| `wave selfupdate` | Update MacWave itself | When you want a newer MacWave | |
| `wave list` | List the installed packages and their versions | Seeing what you have installed | `wave list -a` does the same |
| `wave info <pkg_name>` | Show which version of a package you have installed (prints `None` when it is not installed) | Not knowing whether — or which version — you installed | |
| `wave search <pkg_name>` | Search for a package (matches part of the name) | Checking whether `wave` has that package | |
| `wave uninstall <pkg_name>` | Remove a package | Uninstalling software | `wave uninstall <pkg_name>@<pkg_version>` removes one specific version |

For more, run `wave -h`, `wave -h --zh` (Chinese), `wave manual`, or `wave manual --zh` (Chinese).

Note: when you actually run these commands, replace the `<placeholder>` parts with real values.

### Install locations

**The directories below are only our recommendations — you can pick any directory, or a
custom one (recommended first):**

macOS (shared install, recommended): `/opt/macwave`
macOS (single user): `~/.local/macwave`
Linux (shared install, recommended): `/home/linuxwave/.linuxwave`
Linux (single user): `~/.local/linuxwave`

Note: on Intel Macs we do not recommend `/usr/local` — it may collide with Homebrew's
default prefix on Intel Macs.

**Configuration files live in (the system-wide location always wins):**

**MacWave:**

1. `/opt/macwave_config` — shared install
2. `~/.config/macwave_config` — single-user install

**LinuxWave:**

1. `/etc/linuxwave_config` — shared install
2. `~/.config/linuxwave_config` — single-user install

**Warning: do not edit the configuration files casually — that can make `wave` behave
strangely or in ways you do not expect.**

#### Pros and cons of each directory

Worth a look before choosing: the permission model, how much disk the dependencies take,
and whether the tree can be moved later all differ.

**macOS (MacWave)**

| Directory | Who it is for | Pros | Cons |
| --- | --- | --- | --- |
| **`/opt/macwave` (recommended, default)** | You are an administrator and the machine needs one install | Dependencies exist **once** and are shared by every user (`deps/` is often a few hundred MB); the tree is `root:<admin group>` 775 with setgid directories, so members of the admin group **install packages without sudo**; same mental model as Homebrew (`/opt/homebrew`); independent of `$HOME`, so moving machines, renaming the user or running scripts under `sudo` cannot make it point somewhere else | Needs **one** administrator password at install time; the tree is shared state, so two admins on one machine can affect each other (that is the other side of "one copy of the dependencies"); uninstalling touches files owned by root (the directories are group-writable, so this normally needs no extra sudo) |
| `~/.local/macwave` | No admin password, or you only want it for yourself, or you want to delete it on a whim | **Never needs sudo**; entirely yours, `rm -rf` removes it; writes nothing outside your home | Dependencies are not shared: one copy per user; breaks if `$HOME` changes (renamed account, migrated machine, running under `sudo`); the `PATH` entry has to follow `$HOME` |
| `/usr/local/macwave` | Intel Mac users who live in `/usr/local` | Same shared model as `/opt` (775, setgid) | **Can collide with Homebrew on Intel Macs** (its default prefix is `/usr/local`); on Apple silicon `/usr/local` is *not* where Homebrew lives, so two sets of tools easily end up side by side |
| A custom directory | External volumes, several side-by-side installs | Completely free | You own the permission/sharing model; remember to put `<dir>/bin`, `<dir>/links` and `<dir>/lib` on `PATH` |

Quick reminder: `wave basedir --raw` prints where the current install lives, and
`wave basedir --set <new dir>` moves the whole tree (run `wave transfer --all` first so every
artifact is position-independent).

**Linux (LinuxWave)**

| Directory | Who it is for | Pros | Cons |
| --- | --- | --- | --- |
| **Shared install (`/home/linuxwave/.linuxwave`, recommended)** | Multi-user machines, or anything that runs as a service | The dependencies exist **once**; the tree belongs to a dedicated `linuxwave` account and its **same-named group**, so group members install packages **without sudo**; the config lives in `/etc/linuxwave_config` (`root:linuxwave` 2775); the tree can run under a low-privilege account, so daemons need not be root | Needs one sudo to create the account/group and write `/etc`; **you must log out and back in** afterwards (a group only applies to a new session) or run `newgrp linuxwave`; group members can modify the whole tree, including `lib/wave` itself — that limits "who can influence MacWave/LinuxWave on this box" to that group, but does not remove the ability |
| `~/.local/linuxwave` | Single user, no system directories | No sudo; delete anytime | Dependencies not shared; one copy per user on a multi-user box |
| `/opt/linuxwave` | Single user, but a fixed path is wanted | One sudo at install time, then the tree **and the config belong to you**; fixed path, independent of `$HOME` | **Not shared at all**: other users can read but not install; your distribution's package manager knows nothing about it (upgrades and removal go through `wave`) |
| `/usr/local/linuxwave` | People who follow FHS | The same "owned by the installer" model as `/opt` | Easily mixed with hand-built `make install` output; answering "who installed this `.so`?" gets harder |

> Adding people to a shared install: `sudo usermod -aG linuxwave <user>`, then have them
> log out and back in. For a single service, just run it as the `linuxwave` account — it
> already owns that group.

### Mirrors

If you are in mainland China you most likely need a mirror. For a full mirror, add the
following environment variables to `~/.zshrc` (or `~/.bashrc` if you use bash). A good
mirror will usually tell you which commands to run:

| Variable | What it points at | Default |
| --- | --- | --- |
| `MACWAVE_BOTTLE_DOMAIN` | Prebuilt packages | GitHub Releases |
| `MACWAVE_DEPS_DOMAIN` | Dependency libraries | GitHub Releases |
| `MACWAVE_API_DOMAIN` | Package index | `infosource` on raw.githubusercontent |
| `MACWAVE_SELFUPDATE_DOMAIN` | Self-update data | `Selfupdate` on raw.githubusercontent |
| `MACWAVE_PYTHON_DOMAIN` | The bundled interpreter | `Python` on raw.githubusercontent |
| `MACWAVE_CORE_DOMAIN` | MacWave's own files | `MacWave` on raw.githubusercontent |
| `MACWAVE_PIP_INDEX` | The `pip` index (affects only the three Python dependencies) | `https://pypi.org/simple` |

**The ref segment after `infosource` is not optional:** it is `/HEAD` for MacWave and
`/main` for LinuxWave (the mirror lays files out as `<org>/<repo>/<ref>/…`). Leave it out
and `wave search` / `wave latest` get nothing but 404s when they read the lists.

Run the following to add them:

```zsh
export MACWAVE_BOTTLE_DOMAIN=https://mirror.example.cn/MacWave/bottle
export MACWAVE_DEPS_DOMAIN=https://mirror.example.cn/MacWave/deps
export MACWAVE_API_DOMAIN=https://mirror.example.cn/MacWave/infosource/HEAD
export MACWAVE_SELFUPDATE_DOMAIN=https://mirror.example.cn/MacWave/selfupdate
export MACWAVE_PYTHON_DOMAIN=https://mirror.example.cn/MacWave/python
export MACWAVE_CORE_DOMAIN=https://mirror.example.cn/MacWave/core
export MACWAVE_PIP_INDEX=https://pypi.mirror.example.cn/simple
```

`export` only affects the current terminal; it is gone once you close it. Append the block
to `~/.zshrc` and every terminal inherits it from then on:

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

`MACWAVE_PIP_INDEX` only affects the three Python dependencies `pip` installs
(`requests`, `toml`, `colorama`), so it can point at any PyPI mirror (popular ones in
China include USTC and TUNA).

You only need to run this once. New terminals pick it up by themselves; the trailing
`source` merely makes the current one take effect immediately. Delete any lines you do
not need — fewer lines still work, and an unset variable falls back to the official
address.

If you later want to drop the mirror, delete or comment those lines out.

LinuxWave works the same way: replace `MACWAVE` above with `LINUXWAVE`. Note that Linux
uses `bash` by default.

### Contact

If something goes wrong, open an issue on GitHub or write to `macwaveorg@outlook.com`.

**Have a good surf, waver!**
