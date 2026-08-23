---
layout: single
permalink: /ja/
title: "音声・マルチモーダルAIの研究者"
description: "NAISTの音声AI研究者・教育者。音声処理とマルチモーダル処理に関するオープンソースツール（Nkululeko、Speechain）、チュートリアル、デモを公開しています。"
lang: ja
lang_ref: about
author_profile: true
redirect_from:
  - /ja/about/
  - /ja/about.html
---
> 実践せよ。読むだけで終わらない。

BTA は NAIST の音声 AI 研究者・教育者です。音声分類から ASR、TTS までの音声処理から、音響学やマルチモーダル情報融合に関する研究、教育、学生指導を行っています。下図は、マルチモーダル、音響、音声の関係を示しており、それぞれの概念がより大きな概念に含まれることを表しています。マルチモーダルは、音声、映像、テキストなど複数のモダリティからの情報を統合します。音響学は、音楽・音声・ノイズを含め、音がどのように生成・伝達・知覚されるかという物理的性質を扱います。音声処理は、さまざまな用途のために人間の音声信号を分析し理解することです。

日本語については、日本語能力試験（JLPT）N3を取得（2020年）。来日後も学習を継続しており、下記マインドマップの「日本語」に挙げた教材・ツールは自身の学習のために作成したものです。

<p align="center">
 <img src="../images/research_bta_jp.png" alt="研究領域: 音声、音響、マルチモーダル">
</p>

以下は、BTA の研究、ツール、チュートリアル、コース、論文、その他の関心事をまとめたマインドマップです。ノードをクリックすると詳細を確認できます。
<pre class="mermaid">
mindmap
  root((BTA))
    ツール
      Nkululeko
      Speechain
      PaperRAG
      Audiokit
      Sherox
    チュートリアル
      ShellとLinux
      Pythonチュートリアル
      Shell拡張
    コース
      音声認識コース
      信号処理のためのPython
      マルチモーダル処理
      基礎数学
    論文
      Speech Communication
      ICASSP
      Interspeech
      O-COCOSDA
      APSIPA
    日本語
      Ayo Belajar Bahasa Jepang
      みんなの日本語
      仕事のための日本語
      漢字ドリル
      ことば
      JLPT
      JED
      Wani Kanji
    イスラム
      預言者物語
      アルバイン・ナワウィ
</pre>

<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';

const LINKS = {
  '研究':                    '/ja/research/',
  'ツール':                  '/tools/',
  'チュートリアル':          '/tutorials/',
  '論文':                    '/publications/',
  'Nkululeko':               'https://nkululeko.readthedocs.io/en/latest/',
  'Speechain':               'https://bagustris.github.io/speechain',
  'PaperRAG':                'https://bagustris.github.io/paperrag',
  'Audiokit':                'https://github.com/bagustris/audiokit',
  'Sherox':                  'https://github.com/bagustris/sherox',
  'ShellとLinux':            'https://bagustris.github.io/tutorial-shell',
  'Pythonチュートリアル':    'https://bagustris.github.io/python-tutorial',
  'Shell拡張':               'https://bagustris.github.io/shell-extras',
  '音声認識コース':          'https://bagustris.github.io/speech-recognition-course',
  '信号処理のためのPython':  'https://bagustris.github.io/python-for-signal-processing',
  'マルチモーダル処理':      'https://bagustris.github.io/multisensory',
  '基礎数学':                'https://bagustris.github.io/matematika/',
  'Email':                   'mailto:bagustris@outlook.com',
  'GitHub Profile':          'https://github.com/bagustris',
  'Google Scholar':          'https://scholar.google.com/citations?user=xuiLAewAAAAJ&hl=en',
  'CV':                      '/cv/',
  'Ayo Belajar Bahasa Jepang': 'https://bagustris.github.io/bbj/',
  'みんなの日本語':          'https://bagustris.github.io/minna-no-nihongo/',
  '仕事のための日本語':      'https://bagustris.github.io/japanese-for-work/',
  '漢字ドリル':              'https://bagustris.github.io/kanji-drill/',
  'ことば':                  'https://bagustris.github.io/kotoba/',
  'JLPT':                    'https://bagustris.github.io/jlpt/',
  'JED':                     'https://bagustris.github.io/jed/',
  'Wani Kanji':              'https://bagustris.github.io/wanikanji/',
  '預言者物語':              'https://bagustris.github.io/kisah-nabi',
  'アルバイン・ナワウィ':    'https://bagustris.github.io/arbain-nawawi',
  'ブログ':                  'https://bagustris.blogspot.com',
  '学位論文':                'https://dspace.jaist.ac.jp/dspace/bitstream/10119/17472/2/paper.pdf',
};

mermaid.initialize({ startOnLoad: false, securityLevel: 'loose' });

mermaid.run({ querySelector: '.mermaid' }).then(() => {
  document.querySelectorAll('.mermaid svg').forEach(svg => {
    svg.querySelectorAll('foreignObject p, text').forEach(el => {
      const label = el.textContent.trim();
      const href = LINKS[label];
      if (!href) return;
      const node = el.closest('g');
      if (!node) return;
      node.style.cursor = 'pointer';
      node.addEventListener('click', e => {
        e.stopPropagation();
        href.startsWith('/') || href.startsWith('mailto:')
          ? (window.location.href = href)
          : window.open(href, '_blank');
      });
    });
  });
});
</script>
