# 송도 천년의미소 — 네이버 블로그 자동 연동 버전

네이버 블로그 `songdo1000miso`의 RSS를 GitHub Actions가 서버 쪽에서 읽어
`data/blog-posts.json`을 갱신한 뒤 GitHub Pages에 배포하는 구조입니다.

## 작동 방식

1. 네이버 블로그에 새 포스트 작성
2. GitHub Actions가 6시간마다 RSS 확인
3. `scripts/fetch_naver_blog.py`가 최신 글을 JSON으로 저장
4. 홈페이지 `index.html`이 JSON을 읽어 최신 콘텐츠 카드를 표시
5. 카드 클릭 시 네이버 블로그 원문으로 이동

브라우저가 네이버 RSS를 직접 호출하지 않으므로 CORS 문제와 API 비밀키 노출을 피할 수 있습니다.

## 1. GitHub에 업로드

ZIP을 풀고 **안의 파일 전체**를 repository의 root에 올리세요.

반드시 아래 구조가 보여야 합니다.

```
.github/
  workflows/
    sync-blog.yml
scripts/
  fetch_naver_blog.py
data/
  blog-posts.json
assets/
  logo.png
index.html
.nojekyll
README.md
```

`.github`은 숨김 폴더처럼 보일 수 있지만 반드시 같이 올라가야 합니다.

## 2. GitHub Pages 설정 변경

Repository → `Settings` → `Pages`

**Build and deployment / Source**를:

`GitHub Actions`

로 선택하세요.

예전에 `Deploy from a branch`로 설정했다면 이번 버전에서는 `GitHub Actions` 방식으로 바꾸는 것을 권장합니다.

## 3. Actions 쓰기 권한 확인

Repository → `Settings` → `Actions` → `General`

아래쪽 **Workflow permissions**에서 쓰기 권한이 차단되어 있다면
`Read and write permissions`를 선택하고 저장하세요.

워크플로 파일 자체에도 `contents: write`, `pages: write`, `id-token: write`가 지정되어 있습니다.

## 4. 최초 수동 실행

Repository → `Actions`

왼쪽에서:

`Sync Naver Blog and Deploy Pages`

선택 → `Run workflow` → `Run workflow`

실행이 끝나면 초록색 체크가 표시됩니다.

그 후 GitHub Pages 주소를 새로고침하면 실제 네이버 블로그 최신 글이 표시됩니다.

## 자동 갱신 주기

현재 워크플로는 약 **6시간마다** 실행되도록 되어 있습니다.

```yaml
- cron: "17 */6 * * *"
```

GitHub scheduled workflow는 정확히 정각 실행을 보장하지 않으므로 약간 늦어질 수 있습니다.

## 바로 갱신하고 싶을 때

블로그 글을 작성한 직후 홈페이지에도 바로 반영하려면:

`Actions` → `Sync Naver Blog and Deploy Pages` → `Run workflow`

를 누르면 됩니다.

## RSS 주소

현재 설정:

`https://rss.blog.naver.com/songdo1000miso.xml`

네이버는 RSS 접근 시 HTTPS 사용을 권장하고 있습니다.

## 참고

- RSS에 포함되는 글 수/본문/이미지는 네이버가 제공하는 데이터 범위에 따라 달라질 수 있습니다.
- 썸네일은 RSS description 안에 `<img>`가 있을 때 자동 추출하도록 구현했습니다.
- 썸네일을 RSS에서 제공하지 않는 글은 홈페이지의 기본 그래픽 배경이 표시됩니다.
- 홈페이지에는 제목, 날짜, 카테고리, 요약, 썸네일, 원문 링크가 표시됩니다.
- 블로그 글 원문 전체를 홈페이지에 복제하지 않고 원문 링크로 연결하도록 구성했습니다.
