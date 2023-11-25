# Eastern Min corpus / 閩東語語料庫

詳見 [Wiki](https://github.com/MindongLab/cdo-corpus/wiki)。

Visit our [Wiki page](https://github.com/MindongLab/cdo-corpus/wiki) for more information.

## Directory tree 目錄結構

### Plaintext 純文本語料

- `/plaintext` 純文本語料的母目錄，下含語句、詩歌、文章、書籍等類。
  - `/.../word-alignment` 以XML格式標註、精度爲詞的純文本語料。

### Spoken corpus 有聲語料

- `/essay` 朗讀文章。
- `/music` 歌曲。
- `/opera` 戲曲。請參閱[相關工作流](https://github.com/MindongLab/cdo-corpus/projects/3)。
  - `/.../Min opera` 閩劇（包括其選段）。
- `/poem` 詩歌、謠讖。
- `/video` 影片。請參閱[相關工作流](https://github.com/MindongLab/cdo-corpus/projects/1)。
- `/sentences` 語句。請參閱[句料分類規範](https://github.com/MindongLab/cdo-corpus/wiki/Info-of-Sentences-%E5%8F%A5%E6%96%99%E8%B3%87%E8%A8%8A)。
  - `/.../info.tsv` 語料信息表。查閱、編輯前應看此表，以瞭解語料的整理、標註狀態。
  - `/.../template.etf` ELAN模板。

純文本、有聲語料目錄，除`/sentences`以外，會以語料狀態各設不同的子文件夾：

文件夾名 | 含義
-- | --
Machine-unreadable | 暫未整理出機器可讀的文本。
Working on sentence alignment (cdo) | 正在整理句對齊的閩東語文本。
Sentence-aligned (cdo) | 具備已經句對齊的閩東語文本。
Sentence-aligned (cdo, cmn) | 具備已經句對齊的原語爲閩東語、譯語爲官話的文本。
Sentence-aligned (cmn, cdo) | 具備已經句對齊的原語爲官話、譯語爲閩東語的文本。

### Other 其他材料

- `/audio` 擬用於榕典的音頻文件。請參閱[相關工作流](https://github.com/MindongLab/cdo-corpus/projects/4)。
  - `/.../audio contrib` 用戶貢獻詞彙的音頻文件。
    - `/.../Audio Source.tsv` 音頻信息。
  - `/.../audio contrib sentences` 用戶貢獻詞彙的例句音頻文件。
  - `/.../audio feng` 具備Zingzeu ID的馮愛珍版《福州方言詞典》詞彙音頻。
    - `/.../Audio Prepared for Yng Dieng` 音頻信息。
  - `/.../audio li` 具備Zingzeu ID的李如龍版《福州方言詞典》詞彙音頻。
    - `/.../Audio Prepared for Yng Dieng` 音頻信息。
- `/timing` 記錄志願者的標記工作時長，以資安排任務之參考。
