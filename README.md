# TorrentAutoDownload
Automated script for downloading series from torrent sites with [Transmission client](https://transmissionbt.com/)

## Usage:

#### 1. Extract your login cookie from bh:

![step1](https://github.com/bbkbarbar/TorrentAutoDownload/blob/main/extract_bh_cookie/1.png)

![step2](https://github.com/bbkbarbar/TorrentAutoDownload/blob/main/extract_bh_cookie/2.png)

#### 2. Insert extracted data in your `bh_******.py` script (→ `BITCOOKIE`).

#### 3. Modify the following parameters in `bh_******.py`:
   - `BITCOOKIE`
   - `TITLE`
   - `SEARCH_URL`
   - `LAST_FILE`
   - `DOWNLOAD_DIR`

#### 4. Modify `run_silent.vbs` script according to your working path.

#### 5. Set the Windows Task Scheduler as how often as you want it to check for new torrent(s) availability.

