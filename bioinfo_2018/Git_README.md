----
*Bioinformatics*

*Muyang Huang*

*Last Update: 2018-12-18*

---
# 第10回 Git for Scientists
## [2018-12-18](https://github.com/haruosuz/introBI/tree/master/2018#guest-speaker)

---
## Unix command

**I ran the following command:**

- history


    mkdir git_dir
    cd git_dir/
    git init
    git config --local user.name "Genesis-Hmy"
    git config --local user.email "t18301mh@sfc.keio.ac.jp"
    git config --list
    git init
    ls
    ls -a
    touch sample
    ls
    git status
    touch sample.txt
    ls
    rm sample
    ls
    git status
    git add sample.txt
    git commit -m "Create sample.txt for lesson"
    git status
    git log
    vim sample.txt
    git status
    git diff
    git commit -m "Write about today"
    git status
    git add sample.txt
    git status
    git reset .
    git status

- terminal


    cd
    # ホームディレクトリに移動する。
    # 以下globalを試す。
    git config --global user.email
    ssh-keygen -t rsa -C "t18301mh@sfc.keio.ac.jp"
    : ^C
    ls ~/.ssh
    git config --global user.email
    ssh-keygen -t rsa -C "t18301mh@sfc.keio.ac.jp"
    :
    :
    :
    clip < ~/.ssh/id_rsa.pub
    find git
    git





    git config --local user.name "Genesis-Hmy"
    # localでuser.nameを指定。
    mkdir git_dir
    # ディレクトリを作る。
    cd git_dir/
    # ディレクトリに移動。
    git init
    git config --local user.name "Genesis-Hmy"
    # localでuser.nameを指定。
    git config --local user.email "t18301mh@sfc.keio.ac.jp"
    # localでuser.emailを指定。
    git config --list
    # 設定の確認をする。
    git init
    # レポジトリを作る。
    ls
    # 空であることを確認。
    ls -a
    # 隠しファイルもないことを確認。
    touch sample
    # sampleディレクトリを作る。
    ls
    git status
    # statusを確認。
    touch sample.txt
    # 新しいファイルをtouchで作る。
    ls
    rm sample
    # sampleディレクトリを削除する。
    ls
    git status
    # statusを確認。
    git add sample.txt
    git commit -m "Create sample.txt for lesson"
    # このコミットが何かを表すメッセージ。
    git status
    # statusを確認する。
    git log
    # logを確認する。
    vim sample.txt
    # vim エディターでファイルを編集し、1行加える。
    git status
    # 変更があることがわかる。
    git diff
    # 変更内容を確認する。
    git commit -m "Write about today"
    # addするまえに、git commitすると怒られる。
    git status
    # statusを確認する。
    git add sample.txt
    # addする。
    git status
    # statusで現状を確認する。
    git reset sample.txt
    # git addを取り消す。
    git status
    # statusで確認する。

---
### memorandum

- git addを取り消す。
 - 今回の場合:
        git reset HEAD sample.txt
   で消すのが一番無難。
   <br>sample.txtはgitのステージングから取り除かれ、addする前の状態に戻る。
 - その他:
   - git reset sample.txt:
   <br>HEADは省略しても良い。
   - git reset HEAD .:
   <br>カレントディレクトリ以下全てのファイルを対象に戻す。
   - git rm --cached sample.txt
   - git rm --cached sample_dir
   - git rm sample.txt

---
### Result

```
net41-dhcp103:~ huang$ cd
net41-dhcp103:~ huang$ git config --global user.email
net41-dhcp103:~ huang$ ssh-keygen -t rsa -C "t18301mh@sfc.keio.ac.jp"
Generating public/private rsa key pair.
Enter file in which to save the key (/Users/huang/.ssh/id_rsa): ^C
net41-dhcp103:~ huang$ ls ~/.ssh
known_hosts
net41-dhcp103:~ huang$ git config --global user.email
net41-dhcp103:~ huang$ ssh-keygen -t rsa -C "t18301mh@sfc.keio.ac.jp"
Generating public/private rsa key pair.
Enter file in which to save the key (/Users/huang/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /Users/huang/.ssh/id_rsa.
Your public key has been saved in /Users/huang/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:v9RfWGbLx5sCfvp+LdRL+dc5qRc3u9dS0N+DZK+U/co t18301mh@sfc.keio.ac.jp
The key's randomart image is:
+---[RSA 2048]----+
|                 |
|                 |
|               . |
|             o. .|
|        S   o =oB|
|         . o +o#B|
|          + +.++^|
|         . o *oX%|
|          ..=+EB=|
+----[SHA256]-----+
net41-dhcp103:~ huang$ clip < ~/.ssh/id_rsa.pub
-bash: clip: command not found
net41-dhcp103:~ huang$ find git
find: git: No such file or directory
net41-dhcp103:~ huang$ git
usage: git [--version] [--help] [-C <path>] [-c <name>=<value>]
           [--exec-path[=<path>]] [--html-path] [--man-path] [--info-path]
           [-p | --paginate | -P | --no-pager] [--no-replace-objects] [--bare]
           [--git-dir=<path>] [--work-tree=<path>] [--namespace=<name>]
           <command> [<args>]

These are common Git commands used in various situations:

start a working area (see also: git help tutorial)
   clone      Clone a repository into a new directory
   init       Create an empty Git repository or reinitialize an existing one

work on the current change (see also: git help everyday)
   add        Add file contents to the index
   mv         Move or rename a file, a directory, or a symlink
   reset      Reset current HEAD to the specified state
   rm         Remove files from the working tree and from the index

examine the history and state (see also: git help revisions)
   bisect     Use binary search to find the commit that introduced a bug
   grep       Print lines matching a pattern
   log        Show commit logs
   show       Show various types of objects
   status     Show the working tree status

grow, mark and tweak your common history
   branch     List, create, or delete branches
   checkout   Switch branches or restore working tree files
   commit     Record changes to the repository
   diff       Show changes between commits, commit and working tree, etc
   merge      Join two or more development histories together
   rebase     Reapply commits on top of another base tip
   tag        Create, list, delete or verify a tag object signed with GPG

collaborate (see also: git help workflows)
   fetch      Download objects and refs from another repository
   pull       Fetch from and integrate with another repository or a local branch
   push       Update remote refs along with associated objects

'git help -a' and 'git help -g' list available subcommands and some
concept guides. See 'git help <command>' or 'git help <concept>'
to read about a specific subcommand or concept.
net41-dhcp103:~ huang$





net41-dhcp103:~ huang$ git config --local user.name "Genesis-Hmy"
fatal: --local can only be used inside a git repository
net41-dhcp103:~ huang$ mkdir git_dir
net41-dhcp103:~ huang$ cd git_dir/
net41-dhcp103:git_dir huang$ git init
Initialized empty Git repository in /Users/huang/git_dir/.git/
net41-dhcp103:git_dir huang$ git config --local user.name "Genesis-Hmy"
net41-dhcp103:git_dir huang$ git config --local user.email "t18301mh@sfc.keio.ac.jp"
net41-dhcp103:git_dir huang$ git config --list
credential.helper=osxkeychain
user.name=Muyang_Huang
user.mail=t18301mh@sfc.keio.ac.jp
core.repositoryformatversion=0
core.filemode=true
core.bare=false
core.logallrefupdates=true
core.ignorecase=true
core.precomposeunicode=true
user.name=Genesis-Hmy
user.email=t18301mh@sfc.keio.ac.jp
net41-dhcp103:git_dir huang$ git init
Reinitialized existing Git repository in /Users/huang/git_dir/.git/
net41-dhcp103:git_dir huang$ ls
net41-dhcp103:git_dir huang$ ls -a
.	..	.git
net41-dhcp103:git_dir huang$ touch sample
net41-dhcp103:git_dir huang$ ls
sample
net41-dhcp103:git_dir huang$ git status
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)

	sample

nothing added to commit but untracked files present (use "git add" to track)
net41-dhcp103:git_dir huang$ touch sample.txt
net41-dhcp103:git_dir huang$ ls
sample		sample.txt
net41-dhcp103:git_dir huang$ rm sample
net41-dhcp103:git_dir huang$ ls
sample.txt
net41-dhcp103:git_dir huang$ git status
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)

	sample.txt

nothing added to commit but untracked files present (use "git add" to track)
net41-dhcp103:git_dir huang$ git add sample.txt
net41-dhcp103:git_dir huang$ git commit -m "Create sample.txt for lesson"
[master (root-commit) a0208cf] Create sample.txt for lesson
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 sample.txt
net41-dhcp103:git_dir huang$ git status
On branch master
nothing to commit, working tree clean
net41-dhcp103:git_dir huang$ git log
commit a0208cf281d8f750df27b836f82bc9b402798e6c (HEAD -> master)
Author: Genesis-Hmy <t18301mh@sfc.keio.ac.jp>
Date:   Tue Dec 18 14:05:07 2018 +0900

    Create sample.txt for lesson
net41-dhcp103:git_dir huang$ vim sample.txt
net41-dhcp103:git_dir huang$ git status
On branch master
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

	modified:   sample.txt

no changes added to commit (use "git add" and/or "git commit -a")
net41-dhcp103:git_dir huang$ git diff
diff --git a/sample.txt b/sample.txt
index e69de29..18249f3 100644
--- a/sample.txt
+++ b/sample.txt
@@ -0,0 +1 @@
+Hello world.
net41-dhcp103:git_dir huang$ git commit -m "Write about today"
On branch master
Changes not staged for commit:
	modified:   sample.txt

no changes added to commit
net41-dhcp103:git_dir huang$ git status
On branch master
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

	modified:   sample.txt

no changes added to commit (use "git add" and/or "git commit -a")
net41-dhcp103:git_dir huang$ git add sample.txt
net41-dhcp103:git_dir huang$ git status
On branch master
Changes to be committed:
  (use "git reset HEAD <file>..." to unstage)

	modified:   sample.txt

net41-dhcp103:git_dir huang$ git reset .
Unstaged changes after reset:
M	sample.txt
net41-dhcp103:git_dir huang$ git status
On branch master
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

	modified:   sample.txt

no changes added to commit (use "git add" and/or "git commit -a")
net41-dhcp103:git_dir huang$
```

---
----------
