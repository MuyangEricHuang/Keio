----
*Bioinformatics*

*Muyang Huang*

*Last Update: 2018-10-23*

---
# 第01回 Introduction
## [2018-09-25](https://github.com/haruosuz/introBI/tree/master/2018#introduction)

---
## Unix command

**I ran the following command:**

    bash
    cd
    pwd
    ls
    date
    git clone https://github.com/vsbuffalo/bds-files
    <!-- 教科書Bioinformatics Data Skillsの補足資料Supplementary Materialを取得する. -->
    ls -l bds-files/
    <!-- ls -lコマンドでディレクトリの詳細情報を表示する。 -->
    wget https://dl.dropboxusercontent.com/s/h1uqihudiw1uioy/markdown.md
    curl -O https://dl.dropboxusercontent.com/s/h1uqihudiw1uioy/markdown.md
    <!-- ターミナルでコマンドを実行し、Markdown文書をダウンロードする。 -->
    atom markdown.md
    <!-- テキストエディタ「Atom」でファイルを開く。 -->

---
### memorandum

バイオインフォマティクスの研究対象:
- オーミクス：ゲノミクス、トランスクリプトミクス、 プロテオミクス、メタボロミクス。
- ヒトゲノム。
- 環境・ヒトの微生物群集をメタゲノム解析。

ls -lコマンドでディレクトリの詳細情報を表示する。

Markdown文書のプレビュー（Control + Shift + M）

---
### Reference

[Bioinformatics](https://github.com/haruosuz/books/tree/master/bbs#11-from-data-to-knowledge-the-aim-of-bioinformatics)

[bioinformatics | バイオインフォマティクス | 生物情報科学](https://bi.biopapyrus.jp/)

[Bioinformatician](http://blog.fejes.ca/?p=2418)

[誰もが“バイオインフォマティシャン”の時代](http://www.natureasia.com/ja-jp/ndigest/v12/n1/%E8%AA%B0%E3%82%82%E3%81%8C%26ldquo%3B%E3%83%90%E3%82%A4%E3%82%AA%E3%82%A4%E3%83%B3%E3%83%95%E3%82%A9%E3%83%9E%E3%83%86%E3%82%A3%E3%82%B7%E3%83%A3%E3%83%B3%26rdquo%3B%E3%81%AE%E6%99%82%E4%BB%A3/59368)

[Bioinformatics Research](https://github.com/haruosuz/books/tree/master/bbs#13-principal-applications-of-bioinformatics)

[オーミクス](https://ja.wikipedia.org/wiki/%E3%82%AA%E3%83%BC%E3%83%9F%E3%82%AF%E3%82%B9)

[ヒトゲノム](https://ja.wikipedia.org/wiki/%E3%83%92%E3%83%88%E3%82%B2%E3%83%8E%E3%83%A0)

[メタゲノム解析](https://ja.wikipedia.org/wiki/%E3%83%A1%E3%82%BF%E3%82%B2%E3%83%8E%E3%83%9F%E3%82%AF%E3%82%B9)

[λ18](http://classroom.sfc.keio.ac.jp/class/l-to/l-18.html)

[UNIXコマンド入門 [一般ユーザー編] (全24回) - プログラミングならドットインストール](https://dotinstall.com/lessons/basic_unix_v2)

[ターミナル](https://techacademy.jp/magazine/5155)

[教科書Bioinformatics Data Skills](https://github.com/haruosuz/books/blob/master/bds/README.md)

[補足資料Supplementary Material](https://github.com/vsbuffalo/bds-files/)

[Markdown記法入門 (全13回) - プログラミングならドットインストール](https://dotinstall.com/lessons/basic_markdown_v2)

[Atom入門 (全15回) - プログラミングならドットインストール](https://dotinstall.com/lessons/basic_atom_v2)

[テキストエディタ「Atom」](https://webkaru.net/dev/cat/atom/)

[Markdown文書のプレビュー（Control + Shift + M）](https://dotinstall.com/lessons/basic_atom/30511)

---
# 第02回 Managing a Bioinformatics Project
## [2018-10-02](https://github.com/haruosuz/introBI/tree/master/2018#2018-10-02)

---
## Unix command

**I ran the following command:**

    bash
    mkdir ~/projects
    cd ~/projects/
    <!-- プロジェクト・ディレクトリを作成し移動する。 -->
    mkdir zmays-snps
    cd zmays-snps
    mkdir data
    mkdir data/seqs scripts analysis
    ls -l
    touch README data/README
    <!-- touchコマンドでサイズが0の空ファイルを作成する。 -->
    cd data
    touch seqs/zmays{A,B,C}_R{1,2}.fastq
    <!-- 3つのサンプル（zmaysA, zmaysB, zmaysC）毎にペア（R1, R2）の空データファイルを作成する。 -->
    ls seqs/
    ls seqs/zmaysB*
    <!-- ワイルドカードのアスタリスク（\*）を用いて、サンプル名zmaysBを持つ全てのファイルを表示する。 -->
    ls seqs/zmaysB*fastq
    ls seqs/zmaysB_R?.fastq
    <!-- 偶然の一致を避けるために、ワイルドカードを可能な限り限定する。例えば、zmaysB*の代わりに、zmaysB*fastqまたはzmaysB_R?.fastqを用いる（?は任意の1文字）。 -->
    cd seqs/
    ls zmays[AB]\_R1.fastq
    ls zmays[A-B]\_R1.fastq
    <!-- 文字列[AB]や文字の範囲[A-B]にマッチするワイルドカードを用いて、サンプルCを排除する。 -->

---
### memorandum

プロジェクトの全ファイルを1つのディレクトリに格納する:
- data/ディレクトリにデータを格納する。
- scripts/ディレクトリにスクリプトを格納する。
- analysis/ディレクトリに解析結果を格納する。

絶対パス（例 /home/vinceb/projects/zmays-snps/data/input.txt）ではなく、相対パス（例 ../data/input.txt）で指定する。

ファイル（ディレクトリ）名には、スペース（空白）を使わない、英数字かアンダースコアかダッシュ（ A-z a-z 0-9 _ - ）を使う、拡張子を付ける。（例. human_genes_2015-07-07.fasta）

プロジェクトの情報をプレーンテキスト形式のREADMEファイルに記録する。プレーンテキストはコマンドラインから簡単に読込・検索・編集できる。
- READMEファイルはプロジェクトの主ディレクトリに格納する。
- data/READMEファイルに、data/ディレクトリのデータファイルの説明（いつ・どこから・どのようにダウンロードしたのか）を記載する。
- touchコマンドでサイズが0の空ファイルを作成する。

プロジェクトをサブプロジェクトに分割するディレクトリを作成。

ファイル処理を自動化するために、データをサブディレクトリに編成し、明確で一貫性のあるファイル名を付ける。

ワイルドカードのアスタリスク（\*）を用いて、サンプル名zmaysBを持つ全てのファイルを表示する:

    ls seqs/zmaysB*
- 偶然の一致を避けるために、ワイルドカードを可能な限り限定する。例えば、zmaysB*の代わりに、zmaysB*fastqまたはzmaysB_R?.fastqを用いる（?は任意の1文字）。

文字列[AB]や文字の範囲[A-B]にマッチするワイルドカードを用いて、サンプルCを排除する:

    ls zmays[AB]\_R1.fastq
    ls zmays[A-B]\_R1.fastq

プレーンテキスト形式で書かれたプロジェクト・ノートは、コマンドラインやネットワーク経由で読込・検索・編集できる。

---
### Reference

[計算生物学のプロジェクトの管理法入門 (Noble 2009)](http://5hun.github.io/quickguide_ja/)

[SNP](https://ja.wikipedia.org/wiki/%E4%B8%80%E5%A1%A9%E5%9F%BA%E5%A4%9A%E5%9E%8B)

[絶対パスと相対パス](https://codezine.jp/unixdic/w/%E7%B5%B6%E5%AF%BE%E3%83%91%E3%82%B9%E3%81%A8%E7%9B%B8%E5%AF%BE%E3%83%91%E3%82%B9)

[#05 ディレクトリを移動する (2) | UNIXコマンド入門 (一般ユーザー編) - プログラミングならドットインストール](https://dotinstall.com/lessons/basic_unix/5405)

[スペース](https://ja.wikipedia.org/wiki/%E3%82%B9%E3%83%9A%E3%83%BC%E3%82%B9)

[プレーンテキスト](https://ja.wikipedia.org/wiki/%E3%83%97%E3%83%AC%E3%83%BC%E3%83%B3%E3%83%86%E3%82%AD%E3%82%B9%E3%83%88)

[README](https://ja.wikipedia.org/wiki/%E3%83%AA%E3%83%BC%E3%83%89%E3%83%9F%E3%83%BC)

[touch](https://ja.wikipedia.org/wiki/Touch_%28UNIX%29)

[ワイルドカード](https://ja.wikipedia.org/wiki/%E3%83%AF%E3%82%A4%E3%83%AB%E3%83%89%E3%82%AB%E3%83%BC%E3%83%89_%28%E6%83%85%E5%A0%B1%E5%87%A6%E7%90%86%29)

[#12 ワイルドカードについて | UNIXコマンド入門 (一般ユーザー編) - プログラミングならドットインストール](https://dotinstall.com/lessons/basic_unix/5412)

[#22 ワイルドカードを使ってみよう | UNIXコマンド入門 [一般ユーザー編] - プログラミングならドットインストール](https://dotinstall.com/lessons/basic_unix_v2/41622)

[Markdownノート](https://raw.githubusercontent.com/vsbuffalo/bds-files/master/chapter-02-bioinformatics-projects/notebook.md)

[HTML表示](https://github.com/vsbuffalo/bds-files/blob/master/chapter-02-bioinformatics-projects/notebook.md)

---
---
# 第03回 Unix Shell
## [2018-10-09](https://github.com/haruosuz/introBI/tree/master/2018#2018-10-09)

---
## Unix command

**I ran the following command:**

    bash
    cd ~/bds-files/chapter-03-remedial-unix/
    cat tb1-protein.fasta
    <!-- catコマンドで tb1-protein.fasta ファイルを標準出力する。 -->
    cat tb1-protein.fasta tga1-protein.fasta
    <!-- 複数のファイルを標準出力する。 -->
    cat tb1-protein.fasta tga1-protein.fasta > zea-proteins.fasta
    <!-- 記号>（上書き）や>>（追記）で標準出力をファイルにリダイレクトする。 -->
    ls -lrt
    <!-- 更新日時の逆順にソートする（詳細はman lsを参照）。 -->
    ls -l tb1.fasta leafy1.fasta
    <!-- 存在するファイル（tb1.fasta）は標準出力に、存在しないファイル（leafy1.fasta）は標準エラー出力に送られる。 -->
    ls -l tb1.fasta leafy1.fasta > stdout.txt 2> stderr.txt
    <!-- 記号2>は上書き、2>>は追記。記号>と2>を用いて、標準出力（standard output）と標準エラー出力（standard error）を別のファイルにリダイレクトする。 -->
    cat stdout.txt
    cat stderr.txt
    cat tb1.fasta | grep ">"
    <!-- 標準入力リダイレクト演算子<よりも、Unixパイプ|を使う方が一般的。 -->
    grep ">" tb1.fasta
    <!-- パイプとgrepを用いて、FASTA形式ファイルのヘッダ（>で始まる行）を抽出する。正規表現はクオーテーションで囲む（">"）。grep > tb1.fastaとした場合、シェルは>をリダイレクト演算子と解釈し、ファイルを上書きしてしまう。 -->
    $sleep 60 &
    <!-- コマンドの末尾にアンパサンド（&）を追加して、プログラムをバックグラウンドで実行する。バックグランドで60秒操作できないようにする。 -->
    sleep 60
    <!-- 60秒操作できないようにする。 -->
     # enter control-z
     <!-- Control-zで中断出来る。 -->
    bg
    <!-- bgコマンドを用いてバックグラウンド（background）で再開。 -->
    sleep 60
     # enter control-c
     <!-- Control-c で動作中のプロセスを停止。 -->
    echo $?
    <!-- 終了ステータスの値は、シェルの特殊変数$?に設定される。 -->
    date +%F
    <!-- 時間を表示。 -->
    mkdir $(date +%F)
    <!-- date +%Fコマンドを用いて日付ディレクトリを作成する。 -->
    ls -l
    <!-- このディレクトリ名は年代順にソートされる: -->

---
### memorandum

Unixのシェルを使う。ストリーム、リダイレクト、パイプ、プロセス、コマンド置換を扱う。

catコマンドでfastaファイルを標準出力する。
- 複数のファイルを同時に標準出力できる。

記号>（上書き）や>>（追記）で標準出力をファイルにリダイレクトする:  
- 記号 > （上書き）。
- 記号 >> （追記)。

ls -lrtで更新日時の逆順にソートする（詳細はman lsを参照）。

記号 > と 2> を用いて、標準出力（standard output）と標準エラー出力（standard error）を別のファイルにリダイレクトする:
- 記号> (標準出力)。
- 記号2> (標準エラー出力)。

標準入力リダイレクト演算子<よりも、Unixパイプ|を使う方が一般的。

パイプとgrepを用いて、FASTA形式ファイルのヘッダ（>で始まる行）を抽出する:

    cat tb1.fasta | grep ">"

    grep ">" tb1.fasta
  正規表現はクオーテーションで囲む（">"）。grep > tb1.fastaとした場合、シェルは>をリダイレクト演算子と解釈し、ファイルを上書きしてしまう。

コマンドの末尾にアンパサンド（&）を追加して、プログラムをバックグラウンドで実行する:

    $sleep 60 &
    [1] 86374
  [1]はジョブID、86374はプロセスID（PID）。
- jobsでバックグランド・ジョブを表示する。
- fgでバックグラウンド・プロセスをフォアグラウンド（foreground）へ戻す。
- Control-zキーで中断させたジョブを bg コマンドを用いてバックグラウンド（background）で再開できる。
- Control-c で動作中のプロセスを停止。
- 終了ステータスの値は、シェルの特殊変数$?に設定される。

コマンド置換:
- 時間表示:
      date +%F
- date +%Fコマンドを用いて日付ディレクトリを作成できる。
- ディレクトリ名は年代順にソートされる。

---
### Result

```
>teosinte-branched-1 protein
LGVPSVKHMFPFCDSSSPMDLPLYQQLQLSPSSPKTDQSSSFYCYPCSPP
FAAADASFPLSYQIGSAAAADATPPQAVINSPDLPVQALMDHAPAPATEL
GACASGAEGSGASLDRAAAAARKDRHSKICTAGGMRDRRMRLSLDVARKF
FALQDMLGFDKASKTVQWLLNTSKSAIQEIMADDASSECVEDGSSSLSVD
GKHNPAEQLGGGGDQKPKGNCRGEGKKPAKASKAAATPKPPRKSANNAHQ
VPDKETRAKARERARERTKEKHRMRWVKLASAIDVEAAAASVPSDRPSSN
NLSHHSSLSMNMPCAAA
```

---
---
# 第04回 Bioinformatics Data
## [2018-10-16](https://github.com/haruosuz/introBI/tree/master/2018#2018-10-16)
## [ヒト22番染色体](http://hgdownload.soe.ucsc.edu/goldenPath/hg19/chromosomes/)
## [CaseStudy](https://github.com/haruosuz/introBI/blob/master/2018/CaseStudy.md#grcm38-mouse-reference-genome)

---
## Unix command

**I ran the following command:**

    bash
    cd ~/bds-files/chapter-06-bioinformatics-data/
    wget http://hgdownload.soe.ucsc.edu/goldenPath/hg19/chromosomes/chr22.fa.gz
    <!-- wgetを用いて、ヒト22番染色体をダウンロードする。 -->
    man wget
    <!-- man wgetでオプション一覧を見る。 -->
    curl http://hgdownload.soe.ucsc.edu/goldenPath/hg19/chromosomes/chr22.fa.gz > chr22.fa.gz
    curl -O http://hgdownload.soe.ucsc.edu/goldenPath/hg19/chromosomes/chr22.fa.gz
    <!-- curlは、デフォルトでは標準出力するので、リダイレクトするか、-Oを使う。 -->
    echo "atgc" | md5
    echo "atg" | md5
    <!-- md5プログラムは、任意の文字列を渡すと、MD5値を計算する。 -->
    diff -u gene-1.bed gene-2.bed
    <!-- diffコマンドで gene-1.bedと gene-2.bed ファイルの差分を出力する。 -->
    echo {A,C,G,T}{A,C,G,T} > word2.txt
    gzip word2.txt
    <!-- gzipコマンドで圧縮。 -->
    gunzip word2.txt.gz
    <!-- gunzipコマンドで解凍。 -->
    gzip -c word2.txt > word2.txt.gz
    <!-- -cオプションを用いて圧縮の結果を標準出力に書き出す。 -->
    gunzip -c word2.txt.gz > word2.duplicate.txt
    <!-- -cオプションを用いて解凍の結果を標準出力に書き出す。 -->
    gunzip -c chr22.fa.gz > chr22.fa

    ls -lh chr22*
    <!-- ヒト22番染色体のデータを解凍し、ファイルサイズを確認する。 -->
    echo {A,C,G,T} | gzip > word.txt.gz
    <!-- gzipを用いて、echoの出力を、ディスクに書き込む前に、圧縮する。 -->
    gzip -c word2.txt >> word.txt.gz
    <!-- 解凍しないで圧縮ファイルに結合する。 -->
    gzcat chr22.fa.gz | grep ">"
    zgrep ">" chr22.fa.gz
    zgrep --color -i -n "ACGTACGTACGT" chr22.fa.gz
    <!-- 圧縮ファイルを直接操作できるコマンド: zgrep, gzcat, zdiff, zless。 -->

---

### memorandum

wgetとcurlは、データをウェブからダウンロードするプログラム。
- wgetを用いて、ヒト22番染色体をダウンロードする:
- man wgetでオプション一覧を見る:
      man wget
- curlは、デフォルトでは標準出力するので、リダイレクトするか、-Oを使う:
      curl http://hgdownload.soe.ucsc.edu/goldenPath/hg19/chromosomes/chr22.fa.gz > chr22.fa.gz
      curl -O http://hgdownload.soe.ucsc.edu/goldenPath/hg19/chromosomes/chr22.fa.gz

チェックサムで転送データの整合性を検証:
- md5プログラムは、任意の文字列を渡すと、MD5値を計算する。

データの違いを見る:
- diffコマンドで gene-1.bedと gene-2.bed ファイルの差分を出力する:
      diff -u gene-1.bed gene-2.bed

データの圧縮:
- gzipコマンドで圧縮。
- gunzipコマンドで解凍。
- -cオプションを用いて圧縮・解凍の結果を標準出力に書き出す:
      gzip -c word2.txt > word2.txt.gz
      gunzip -c word2.txt.gz > word2.duplicate.txt
- ヒト22番染色体のデータを解凍し、ファイルサイズを確認する:
      gunzip -c chr22.fa.gz > chr22.fa

      ls -lh chr22*      
- gzipを用いて、echoの出力を、ディスクに書き込む前に、圧縮する:
      echo {A,C,G,T} | gzip > word.txt.gz
- 解凍しないで圧縮ファイルに結合する:
      gzip -c word2.txt >> word.txt.gz

圧縮ファイルを直接操作できるコマンド:
- zgrep
- gzcat
- zdiff
- zless

---
### CaseStudy

```
mkdir -p ~/projects/data/GRCm38
cd ~/projects/data/GRCm38/
wget ftp://ftp.ensembl.org/pub/release-94/fasta/mus_musculus/dna/Mus_musculus.GRCm38.dna.chromosome.MT.fa.gz
wget ftp://ftp.ensembl.org/pub/release-94/fasta/mus_musculus/dna/CHECKSUMS
zgrep "^>" Mus_musculus.GRCm38.dna.chromosome.MT.fa.gz
sum Mus_musculus.GRCm38.dna.chromosome.MT.fa.gz
grep "Mus_musculus.GRCm38.dna.chromosome.MT.fa.gz" CHECKSUMS
shasum Mus_musculus.GRCm38.dna.chromosome.MT.fa.gz
```

#### Result

```
## Genome Data

Mouse (*Mus musculus*) reference genome version GRCm38 (Ensembl release 94) was downloaded on 2018-10-16, using:

    wget ftp://ftp.ensembl.org/pub/release-94/fasta/mus_musculus/dna/Mus_musculus.GRCm38.dna.chromosome.MT.fa.gz

## SHA-1 Sums

 - `Mus_musculus.GRCm38.dna.chromosome.MT.fa.gz`: b75f036ca9554688789b00f64328964c295aedec
```
---
---
# 第05回 Unix Data Tools
## [2018-10-23](https://github.com/haruosuz/introBI/tree/master/2018#2018-10-23)

---
## Unix command

**I ran the following command:**

    bash
    cd ~/bds-files/chapter-07-unix-data-tools/
    <!-- 教科書の補足資料を使うので、ディレクトリを移動する。 -->
    head Mus_musculus.GRCm38.75_chr1.bed
    <!-- headでファイルの先頭部分を表示する。 -->
    head -n 3 Mus_musculus.GRCm38.75_chr1.bed
    tail -n 3 Mus_musculus.GRCm38.75_chr1.bed
    <!-- head/tailの後ろに -n 3 とつけ加えると、最初の3行だけ表示してする。 -->
    less contaminated.
    <!-- lessでcontaminated.fastqファイルを見る。 -->
    # enter q
    <!-- lessを終了するには、qを押す。 -->
    wc Mus_musculus.GRCm38.75_chr1.bed
    <!-- wc（word count）で左から行数、単語数、文字数を表示。 -->
    wc -l Mus_musculus.GRCm38.75_chr1.bed
    <!-- 行数とファイル名を表示。 -->
    wc Mus_musculus.GRCm38.75_chr1.bed Mus_musculus.GRCm38.75_chr1.gtf
    <!-- 2つのファイルの行数とファイル名を表示。 -->
    wc -l Mus_musculus.GRCm38.75_chr1.*
    <!-- Mus_musculus.GRCm38.75_chr1.と名付けられ他ファイルの行数とファイル名を表示。 -->
    ls -l Mus_musculus.GRCm38.75_chr1.bed
    <!-- ls -lでファイルのサイズを確認。 -->
    ls -lh Mus_musculus.GRCm38.75_chr1.bed
    <!-- ls-lh（Human readかも）でヒトが読み易い形式に直してくれる。 -->
    awk -F "\t" '{print NF; exit}' Mus_musculus.GRCm38.75_chr1.bed
    <!-- awkでファイルの列（フィールド）数を表示。 -->
    cut -f 2 Mus_musculus.GRCm38.75_chr1.bed | head -n 3
    <!-- cutでタブ区切りファイルの2列目を抽出。 -->
    cut -f 1 Mus_musculus.GRCm38.75_chr1.bed | head -n 3
    <!-- -f 1 でファイルの1列目を抽出。 -->
    cut -f 1-2 Mus_musculus.GRCm38.75_chr1.bed | head -n 3
    <!-- -f 1-2 でファイルの1-2列目を抽出。 -->
    cut -f 1-3 Mus_musculus.GRCm38.75_chr1.bed | head -n 3
    <!-- -f 1-3 でファイルの1-2列目を抽出。 -->
    cut -f 2-3 Mus_musculus.GRCm38.75_chr1.bed | head -n 3
    <!-- -f 1-2 でファイルの2-3列目を抽出。 -->
    head -n 3 Mus_musculus.GRCm38.75_chr1_bed.csv
    <!-- head -n 3 で最初の3行を表示。 -->
    cut -d"," -f2,3 Mus_musculus.GRCm38.75_chr1_bed.csv | head -n 3
    <!-- CSVファイルだとスペース（空白）ではなく、コンマ（,）で区切られているので、cut -dで区切り文字を指定する。 -->
    cut -d"," -f2,3 Mus_musculus.GRCm38.75_chr1_bed.csv
    grep -v "^#" Mus_musculus.GRCm38.75_chr1.gtf | cut -f 1-8 | head -n3
    grep -v "^#" Mus_musculus.GRCm38.75_chr1.gtf | cut -f 1-8 | column -t | head -n3
    <!-- column -tでタブ区切りファイルの出力を整形。 -->
    ls
    grep "Olfr" Mus_musculus.GRCm38.75_chr1_genes.txt
    <!-- 1番染色体の全タンパク質のEnsembl遺伝子識別子と遺伝子名が含まれている Mus_musculus.GRCm38.75_chr1_genes.txtファイルで"Olfr"を含む遺伝子群をgrepで見つける。 -->
    grep --color "Olfr" Mus_musculus.GRCm38.75_chr1_genes.txt
    <!-- grep --colorでマッチング部分を色付けする。 -->
    grep -v "Olfr" Mus_musculus.GRCm38.75_chr1_genes.txt
    <!-- grep -vでマッチしない行を返す。 -->
    cat example.txt
    grep -v bioinfo example.txt
    <!-- これだけだとbioinformaticsと名付けられたファイルもマッチしてしまう。 -->
    grep -v -w bioinfo example.txt
    <!-- grep -wで（空白で囲まれた）単語全体にマッチする: -->
    cat example.bed
    <!-- パターンにマッチした行の前（-B）、後（-A）、前後（-C）を出力する: -->
    grep -B2 "chr2" example.bed
    <!-- マッチしたchr2とその2行前のデータを出力する。 -->
    grep -A1 "chr2" example.bed
    <!-- マッチしたchr2とその1行後のデータを出力する。 -->
    grep -C1 "chr2" example.bed
    <!-- マッチしたchr2とその前後1行のデータを出力する。 -->

    grep -B1 "AGATCGG" contam.fastq | head -n 6
    grep -c "Olfr" Mus_musculus.GRCm38.75_chr1_genes.txt
    <!-- grep -cで、パターンにマッチした行数を表示。 -->
    grep "Olfr" Mus_musculus.GRCm38.75_chr1_genes.txt
    grep "Olfr" Mus_musculus.GRCm38.75_chr1_genes.txt | wc -l
    grep -c "olfr" Mus_musculus.GRCm38.75_chr1_genes.txt
    grep -ci "olfr" Mus_musculus.GRCm38.75_chr1_genes.txt
    <!-- grep -iで、大文字小文字を区別しない（ignore case）。 -->
    grep -ic "olfr" Mus_musculus.GRCm38.75_chr1_genes.txt
    <!-- -ciと-icの順番は関係無い。 -->
    file Mus_musculus.GRCm38.75_chr1.bed
    <!-- テキストファイルの文字コード（通常はASCII）をfileで確認する。 -->
    file utf8.txt
    file improper.fa
    cat  improper.fa
    cat example.bed
    sort example.bed
    <!-- Sortで行を並べ替える。 -->
    sort -k1,1 -k2,2n example.bed
    <!-- 1列目はアルファベット順でソートし、2列目は数字順でソート。 -->
    sort -k1,1 -k2,2n -r example.bed
    <!-- 全ての列を降順にソート。 -->
    sort -k1,1 -k2,2nr example.bed
    <!-- 2列目の数字だけを降順にソート。 -->
    cat letters.txt
    uniq letters.txt
    <!-- uniqは、連続する重複行を削除して出力する。 -->
    sort letters.txt | uniq
    <!-- letters.txtをソートしてからuniqで連続する重複行を削除して出力する。 -->
    sort letters.txt | uniq -c
    <!-- -cオプションで、重複行の数も表示。 -->
    grep "chr" example.bed
    <!-- grepで"chr"を含むデータをexample.bedから取ってくる。 -->
    grep "chr" example.bed | cut -f 1
    <!-- grepで"chr"を含むデータをexample.bedから取ってきて、第1列を抽出。 -->
    grep "chr" example.bed | cut -f 1 | sort
    <!-- grepで"chr"を含むデータをexample.bedから取ってきて、第1列を抽出し、ソート。 -->
    grep "chr" example.bed | cut -f 1 | sort | uniq -c
    <!-- grepで"chr"を含むデータをexample.bedから取ってきて、第1列を抽出し、ソートし、連続する重複行を削除して出力する。 -->

    grep -v "^#" Mus_musculus.GRCm38.75_chr1.gtf | cut -f3 | sort | uniq -c
    <!-- Unixコマンド（grep, cut, sort, uniq）を組み合わせて、表形式データの列を要約。 -->
    cat example.bed
    cat example_lengths.txt
    sort -k1,1 example.bed > example_sorted.bed
    sort -c -k1,1 example_lengths.txt # verifies is already sorted
    # join -1 <file_1_field> -2 <file_2_field> <file_1> <file_2>
    join -1 1 -2 1 example_sorted.bed example_lengths.txt > example_with_lengths.txt
    cat example_with_lengths.txt
    <!-- join - 共通フィールドをもつ２つのファイルを行単位で結合 -->

---
### memorandum

Unixコマンド（head, tail, less, wc, ls, cut, grep, sort, uniq, join）を用いてテキスト処理を行なう。

Unixコマンドをパイプで繋ぐことにより、データを処理する1行プログラム（ワンライナー）を構築する。

headでファイルの先頭部分を表示し、tailでファイルの末尾部分を表示する:
- 先頭部分を表示:
      head
- 末尾部分を表示:
      tail
- head/tailの後ろに -n 3 とつけ加えると、最初の3行だけ表示してする。
      head -n 3 Mus_musculus.GRCm38.75_chr1.bed
      tail -n 3 Mus_musculus.GRCm38.75_chr1.bed

lessで .fastq ファイルを見る:
- 操作方法:
<br>スペース 	次ページを表示。
<br>b 	前ページを表示。
<br>/文字列 	指定した文字列をカーソル以降で検索。
<br>n 	次検索。
<br>N 	nとは逆方向に次検索。
- ファイルを開いて、/を押して、検索する内容を入力。
- lessでテキスト検索（マッチした部分をハイライト）。
- lessを終了するには、 q を押す。

wc（word count）で行数、単語数、文字数を表示:
- 左から行数、単語数、文字数表示になっている。
      wc -l Mus_musculus.GRCm38.75_chr1.bed
- bedの代わりに*を入れるとMus_musculus.GRCm38.75_chr1.と名付けられた全てのファイルを表示する。
      wc -l Mus_musculus.GRCm38.75_chr1.*

ls -lでファイルのサイズを確認:
- ls-lh（Human readかも）でヒトが読み易い形式に直してくれる。
      ls -lh Mus_musculus.GRCm38.75_chr1.bed

awkでファイルの列（フィールド）数を表示。

cutでタブ区切りファイルの2列目を抽出:
- -f 2 でファイルの2列目を抽出。
      cut -f 2 Mus_musculus.GRCm38.75_chr1.bed
- -f 1-2 でファイルの1-2列目を抽出。
      cut -f 1-2 Mus_musculus.GRCm38.75_chr1.bed | head -n 3
- head -n 3 で最初の3行を表示。
      cut -f 2 Mus_musculus.GRCm38.75_chr1.bed | head -n 3
- CSVファイルだとスペース（空白）ではなく、コンマ（,）で区切られているので、cut -dで区切り文字を指定する。
      head -n 3 Mus_musculus.GRCm38.75_chr1_bed.csv
      cut -d"," -f2,3 Mus_musculus.GRCm38.75_chr1_bed.csv | head -n 3

column -tでタブ区切りファイルの出力を整形:
- 出力されたデータの長さが異なると、次の列が整っていない場合が多い。

1番染色体の全タンパク質のEnsembl遺伝子識別子と遺伝子名が含まれている Mus_musculus.GRCm38.75_chr1_genes.txtファイルで **"Olfr"** を含む遺伝子群を **grep** で見つける:
- grepの後に""でキーワードを入力する。
      grep "Olfr" Mus_musculus.GRCm38.75_chr1_genes.txt
- grep --colorでマッチング部分を色付けする。
      grep --color "Olfr" Mus_musculus.GRCm38.75_chr1_genes.txt
- grep -vでマッチしない行を返す。
      grep -v "Olfr" Mus_musculus.GRCm38.75_chr1_genes.txt
- grep -wで（空白で囲まれた）単語全体にマッチする:
      cat example.txt
      grep -v bioinfo example.txt
  これだけだとbioinformaticsと名付けられたファイルもマッチしてしまう。
      grep -v -w bioinfo example.txt
  これで空白で囲まれたbioinfoだけがマッチする。
- パターンにマッチした行の前（-B）、後（-A）、前後（-C）を出力する:
      cat example.bed
      grep -B2 "chr2" example.bed
  マッチしたchr2とその2行前のデータを出力する。
      grep -A1 "chr2" example.bed
  マッチしたchr2とその1行後のデータを出力する。
      grep -C1 "chr2" example.bed
  マッチしたchr2とその前後1行のデータを出力する。

      grep -B1 "AGATCGG" contam.fastq | head -n 6
- grep -cで、パターンにマッチした行数を表示:
      grep -c "Olfr" Mus_musculus.GRCm38.75_chr1_genes.txt
- grep -iで、大文字小文字を区別しない（ignore case）:
      grep -ci "olfr" Mus_musculus.GRCm38.75_chr1_genes.txt

テキストファイルの文字コード（通常はASCII）をfileで確認する。

Sortで行を並べ替える。
- sortのオプション:
<br>-kで列の範囲（start,end）を指定してソート、-nで数値としてソート。 1列目（染色体 chromosome）でソートし（-k1,1）、1列目が同じもの（例、"chr1"や"chr3"）は2列目で数値としてソートする（-k2,2n）:
      sort -k1,1 -k2,2n example.bed
  1列目はアルファベット順でソートし、2列目は数字順でソート。
- -rオプションで逆順（降順）にソートする:
      sort -k1,1 -k2,2n -r example.bed
  全ての列を降順にソート。
      sort -k1,1 -k2,2nr example.bed
  2列目の数字だけを降順にソート。

uniqは、連続する重複行を削除して出力する:
- -cオプションで、重複行の数も表示:
      sort letters.txt | uniq -c

join - 共通フィールドをもつ２つのファイルを行単位で結合:

    join -1 1 -2 1 example_sorted.bed example_lengths.txt > example_with_lengths.txt
    cat example_with_lengths.txt
  ファイル1の第1フィールドとファイル2の第1フィールドを結合？

---
### Result

```
% bash
bash-4.4$ cd ~/bds-files/chapter-07-unix-data-tools/
bash-4.4$ head Mus_musculus.GRCm38.75_chr1.bed
1       3054233 3054733
1       3054233 3054733
1       3054233 3054733
1       3102016 3102125
1       3102016 3102125
1       3102016 3102125
1       3205901 3671498
1       3205901 3216344
1       3213609 3216344
1       3205901 3207317
bash-4.4$ head -n 3 Mus_musculus.GRCm38.75_chr1.bed
1       3054233 3054733
1       3054233 3054733
1       3054233 3054733
bash-4.4$ tail -n 3 Mus_musculus.GRCm38.75_chr1.bed
1       195240910       195241007
1       195240910       195241007
1       195240910       195241007
bash-4.4$ less contaminated.fastq
<!-- 以下省略。 -->
q
bash-4.4$ wc Mus_musculus.GRCm38.75_chr1.bed
   81226  243678 1698545 Mus_musculus.GRCm38.75_chr1.bed
bash-4.4$ wc -l Mus_musculus.GRCm38.75_chr1.bed
   81226 Mus_musculus.GRCm38.75_chr1.bed
bash-4.4$ wc -l Mus_musculus.GRCm38.75_chr1.*
   81226 Mus_musculus.GRCm38.75_chr1.bed
   81231 Mus_musculus.GRCm38.75_chr1.gtf
    4312 Mus_musculus.GRCm38.75_chr1.gtf.gz
  166769 total
bash-4.4$ wc Mus_musculus.GRCm38.75_chr1.bed Mus_musculus.GRCm38.75_chr1.gtf
   81226  243678 1698545 Mus_musculus.GRCm38.75_chr1.bed
   81231 2385570 26607149 Mus_musculus.GRCm38.75_chr1.gtf
  162457 2629248 28305694 total
bash-4.4$ ls -l Mus_musculus.GRCm38.75_chr1.bed
-rw-r--r--  1 t18301mh  student-mac  1698545  9 25 13:57 Mus_musculus.GRCm38.75_chr1.bed
bash-4.4$ ls -lh Mus_musculus.GRCm38.75_chr1.bed
-rw-r--r--  1 t18301mh  student-mac   1.6M  9 25 13:57 Mus_musculus.GRCm38.75_chr1.bed
bash-4.4$ ls -lh Mus_musculus.GRCm38.75_chr1.bed
-rw-r--r--  1 t18301mh  student-mac   1.6M  9 25 13:57 Mus_musculus.GRCm38.75_chr1.bed
bash-4.4$ awk -F "\t" '{print NF; exit}' Mus_musculus.GRCm38.75_chr1.bed
3
bash-4.4$ cut -f 2 Mus_musculus.GRCm38.75_chr1.bed | head -n 3
3054233
3054233
3054233
bash-4.4$ cut -f 1 Mus_musculus.GRCm38.75_chr1.bed | head -n 3
1
1
1
bash-4.4$ cut -f 1-2 Mus_musculus.GRCm38.75_chr1.bed | head -n 3
1       3054233
1       3054233
1       3054233
bash-4.4$ cut -f 1-3 Mus_musculus.GRCm38.75_chr1.bed | head -n 3
1       3054233 3054733
1       3054233 3054733
1       3054233 3054733
bash-4.4$ cut -f 2-3 Mus_musculus.GRCm38.75_chr1.bed | head -n 3
3054233 3054733
3054233 3054733
3054233 3054733
bash-4.4$
bash-4.4$ head -n 3 Mus_musculus.GRCm38.75_chr1_bed.csv
1,3054233,3054733
1,3054233,3054733
1,3054233,3054733
bash-4.4$ cut -d"," -f2,3 Mus_musculus.GRCm38.75_chr1_bed.csv | head -n 3
3054233,3054733
3054233,3054733
3054233,3054733
bash-4.4$ cut -d"," -f2,3 Mus_musculus.GRCm38.75_chr1_bed.csv
<!-- 以下省略。 -->
bash-4.4$ grep -v "^#" Mus_musculus.GRCm38.75_chr1.gtf | cut -f 1-8 | head -n3
1       pseudogene      gene    3054233 3054733 .       +       .
1       unprocessed_pseudogene  transcript      3054233 3054733 .       +       .
1       unprocessed_pseudogene  exon    3054233 3054733 .       +       .
bash-4.4$ grep -v "^#" Mus_musculus.GRCm38.75_chr1.gtf | cut -f 1-8 | column -t | head -n3
1  pseudogene                          gene         3054233    3054733    .  +  .
1  unprocessed_pseudogene              transcript   3054233    3054733    .  +  .
1  unprocessed_pseudogene              exon         3054233    3054733    .  +  .
bash-4.4$ ls
Mus_musculus.GRCm38.75_chr1.bed         chroms.txt                              greedy_example.txt
Mus_musculus.GRCm38.75_chr1.gtf         contam.fastq                            grep-benchmark.md
Mus_musculus.GRCm38.75_chr1.gtf.gz      contaminated.fastq                      improper.fa
Mus_musculus.GRCm38.75_chr1_bed.csv     example.bed                             lengths.txt
Mus_musculus.GRCm38.75_chr1_genes.txt   example.txt                             letters.txt
Mus_musculus.GRCm38.75_chr1_random.gtf  example2.bed                            mm_gene_names.txt
README.md                               example_lengths.txt                     test.bed
bmark.txt                               genotypes.txt                           utf8.txt
bash-4.4$ grep "Olfr" Mus_musculus.GRCm38.75_chr1_genes.txt
ENSMUSG00000067064      Olfr1416
ENSMUSG00000057464      Olfr1415
ENSMUSG00000042849      Olfr1414
ENSMUSG00000058904      Olfr1413
ENSMUSG00000046300      Olfr1412
ENSMUSG00000062497      Olfr1411
ENSMUSG00000063583      Olfr1410
ENSMUSG00000061616      Olfr12
ENSMUSG00000037924      Olfr16
ENSMUSG00000062527      Olfr1408
ENSMUSG00000058981      Olfr1406
ENSMUSG00000046643      Olfr218
ENSMUSG00000049456      Olfr1404
ENSMUSG00000049605      Olfr418-ps1
ENSMUSG00000045381      Olfr433
ENSMUSG00000047048      Olfr432
ENSMUSG00000050134      Olfr430
ENSMUSG00000049528      Olfr429
ENSMUSG00000059371      Olfr427
ENSMUSG00000046486      Olfr231
ENSMUSG00000051528      Olfr424
ENSMUSG00000055033      Olfr420
ENSMUSG00000050788      Olfr419
ENSMUSG00000066672      Olfr417
ENSMUSG00000059503      Olfr248
ENSMUSG00000051509      Olfr414
ENSMUSG00000066671      Olfr220
bash-4.4$ grep --color  "Olfr" Mus_musculus.GRCm38.75_chr1_genes.txt
<!-- 以下省略。 -->
bash-4.4$ grep -v  "Olfr" Mus_musculus.GRCm38.75_chr1_genes.txt
<!-- 以下省略。 -->
bash-4.4$ cat example.txt
bio
bioinfo
bioinformatics
computational biology
bash-4.4$ grep -v bioinfo example.txt
bio
computational biology
bash-4.4$ grep -v -w bioinfo example.txt
bio
bioinformatics
computational biology
bash-4.4$ cat example.bed
chr1    26      39
chr1    32      47
chr3    11      28
chr1    40      49
chr3    16      27
chr1    9       28
chr2    35      54
chr1    10      19
bash-4.4$ grep -B2 "chr2" example.bed
chr3    16      27
chr1    9       28
chr2    35      54
bash-4.4$ grep -A1 "chr2" example.bed
chr2    35      54
chr1    10      19
bash-4.4$ grep -C1 "chr2" example.bed
chr1    9       28
chr2    35      54
chr1    10      19
bash-4.4$ grep -B1 "AGATCGG" contam.fastq | head -n 6
@DJB775P1:248:D0MDGACXX:7:1202:12362:49613
TGCTTACTCTGCGTTGATACCACTGCTTAGATCGGAAGAGCACACGTCTGAA
--
@DJB775P1:248:D0MDGACXX:7:1202:12782:49716
CTCTGCGTTGATACCACTGCTTACTCTGCGTTGATACCACTGCTTAGATCGG
--
bash-4.4$ grep -c "Olfr" Mus_musculus.GRCm38.75_chr1_genes.txt
27
bash-4.4$ grep "Olfr" Mus_musculus.GRCm38.75_chr1_genes.txt
ENSMUSG00000067064      Olfr1416
ENSMUSG00000057464      Olfr1415
ENSMUSG00000042849      Olfr1414
ENSMUSG00000058904      Olfr1413
ENSMUSG00000046300      Olfr1412
ENSMUSG00000062497      Olfr1411
ENSMUSG00000063583      Olfr1410
ENSMUSG00000061616      Olfr12
ENSMUSG00000037924      Olfr16
ENSMUSG00000062527      Olfr1408
ENSMUSG00000058981      Olfr1406
ENSMUSG00000046643      Olfr218
ENSMUSG00000049456      Olfr1404
ENSMUSG00000049605      Olfr418-ps1
ENSMUSG00000045381      Olfr433
ENSMUSG00000047048      Olfr432
ENSMUSG00000050134      Olfr430
ENSMUSG00000049528      Olfr429
ENSMUSG00000059371      Olfr427
ENSMUSG00000046486      Olfr231
ENSMUSG00000051528      Olfr424
ENSMUSG00000055033      Olfr420
ENSMUSG00000050788      Olfr419
ENSMUSG00000066672      Olfr417
ENSMUSG00000059503      Olfr248
ENSMUSG00000051509      Olfr414
ENSMUSG00000066671      Olfr220
bash-4.4$ grep "Olfr" Mus_musculus.GRCm38.75_chr1_genes.txt | wc -l
      27
bash-4.4$ grep "Olfr" Mus_musculus.GRCm38.75_chr1_genes.txt | wc -l
      27
bash-4.4$ grep -c "olfr" Mus_musculus.GRCm38.75_chr1_genes.txt
0
bash-4.4$ grep -ic "olfr" Mus_musculus.GRCm38.75_chr1_genes.txt
27
bash-4.4$ grep -ci "olfr" Mus_musculus.GRCm38.75_chr1_genes.txt
27
bash-4.4$ file Mus_musculus.GRCm38.75_chr1.bed
Mus_musculus.GRCm38.75_chr1.bed: ASCII text
bash-4.4$ file utf8.txt
utf8.txt: UTF-8 Unicode text
bash-4.4$ file improper.fa
improper.fa: UTF-8 Unicode text
bash-4.4$ cat  improper.fa
>good-sequence
AGCTAGCTACTAGCAGCTACTACGAGCATCTACGGCGCGATCTACG
>bad-sequence
GATCAGGCGACATCGAGCTATCACTACGAGCGAGΑGATCAGCTATT
bash-4.4$ cat example.bed
chr1    26      39
chr1    32      47
chr3    11      28
chr1    40      49
chr3    16      27
chr1    9       28
chr2    35      54
chr1    10      19
bash-4.4$ sort example.bed
chr1    10      19
chr1    26      39
chr1    32      47
chr1    40      49
chr1    9       28
chr2    35      54
chr3    11      28
chr3    16      27
bash-4.4$ sort -k1,1 -k2,2n example.bed
chr1    9       28
chr1    10      19
chr1    26      39
chr1    32      47
chr1    40      49
chr2    35      54
chr3    11      28
chr3    16      27
bash-4.4$ sort -k1,1 -k2,2n -r example.bed
chr3    11      28
chr3    16      27
chr2    35      54
chr1    9       28
chr1    10      19
chr1    26      39
chr1    32      47
chr1    40      49
bash-4.4$ sort -k1,1 -k2,2nr example.bed
chr1    40      49
chr1    32      47
chr1    26      39
chr1    10      19
chr1    9       28
chr2    35      54
chr3    16      27
chr3    11      28
bash-4.4$ cat letters.txt
A
A
B
C
B
C
C
C
bash-4.4$ uniq letters.txt
A
B
C
B
C
bash-4.4$ sort letters.txt | uniq
A
B
C
bash-4.4$ sort letters.txt | uniq -c
   2 A
   2 B
   4 C
bash-4.4$ grep "chr" example.bed | cut -f 1 | sort | uniq -c
   5 chr1
   1 chr2
   2 chr3
bash-4.4$
bash-4.4$ grep "chr" example.bed
chr1    26      39
chr1    32      47
chr3    11      28
chr1    40      49
chr3    16      27
chr1    9       28
chr2    35      54
chr1    10      19
bash-4.4$ grep "chr" example.bed | cut -f 1
chr1
chr1
chr3
chr1
chr3
chr1
chr2
chr1
bash-4.4$ grep "chr" example.bed | cut -f 1 | sort
chr1
chr1
chr1
chr1
chr1
chr2
chr3
chr3
bash-4.4$ grep "chr" example.bed | cut -f 1 | sort | uniq -c
   5 chr1
   1 chr2
   2 chr3
bash-4.4$ cat example.bed
chr1    26      39
chr1    32      47
chr3    11      28
chr1    40      49
chr3    16      27
chr1    9       28
chr2    35      54
chr1    10      19
bash-4.4$ cat example_lengths.txt
chr1    58352
chr2    39521
chr3    24859
bash-4.4$ sort -k1,1 example.bed > example_sorted.bed
bash-4.4$ sort -k1,1 example.bed > example_sorted.bed
bash-4.4$ sort -c -k1,1 example_lengths.txt # verifies is already sorted
bash-4.4$ # join -1 <file_1_field> -2 <file_2_field> <file_1> <file_2>
bash-4.4$ join -1 1 -2 1 example_sorted.bed example_lengths.txt > example_with_lengths.txt
bash-4.4$ cat example_with_lengths.txt
chr1 10 19 58352
chr1 26 39 58352
chr1 32 47 58352
chr1 40 49 58352
chr1 9 28 58352
chr2 35 54 39521
chr3 11 28 24859
chr3 16 27 24859
bash-4.4$
```

---
----------

# Atom (テキストエディタ)
ctrl + Shift + M でMarkdownリアルタイムプレビューを実行する。

----------

# Markdown
見出し（Header）、リスト、コードの書き方

見出しのレベル（1～6）は、#の個数で表す:  

# Header level 1
## Header level 2
### Header level 3
#### Header level 4
##### Header level 5
###### Header level 6

リストは、行頭にダッシュ（-）、アスタリスク（\*）、プラス（+）か、番号ピリオド（1.）を付ける:  

- Windows
- Mac
- Linux

コードは、行頭に「半角スペースを4つ」か「タブを1つ」を追加:  

I ran the following command:

    $ ls

リストの項目内にコードを配置する場合、「半角スペースを8つ」か「タブを2つ」にする。

1. I made `projects` directory using:

        mkdir projects

2. And listed directory contents with:

        ls projects/

----------

# 参考資料
- [Atom (テキストエディタ)](https://ja.wikipedia.org/wiki/Atom_%28テキストエディタ%29)
  - 2015.05.08. [【Mac】Atom凄い！Markdownをリアルタイムでプレビューしながら書ける！HTML出力もできる！](http://wayohoo.com/atom/markdown-function-of-the-atom-is-very-convenient.html)
  - 2014.8.11 [Atom で Windows でも快適 Markdown 環境! | 株式会社バニーホップ](http://www.bunnyhop.jp/tips-20140811/)
  - 2014-05-12 [GitHub製エディタAtomのMarkdownリアルタイムプレビューの仕様 - memorandum](http://slowquery.hatenablog.com/entry/2014/05/12/014310)

- [Markdown](https://ja.wikipedia.org/wiki/Markdown)
  - [Markdown記法入門 (全8回) - プログラミングならドットインストール](http://dotinstall.com/lessons/basic_markdown)
  - [MarkdownでMarkdownの書き方を書いてみた](http://qiita.com/oreo/items/82183bfbaac69971917f)
  - [README.mdファイル。マークダウン記法まとめ | codechord](http://codechord.com/2012/01/readme-markdown/)
  - [ディレクターが知っておいて欲しい10個のMarkdown-マークダウン記法 - PHPサンプル実験室](http://php-fan.org/markdown.html)

----------
