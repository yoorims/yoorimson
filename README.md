# Yoorim Son Researcher Homepage

연구자 PR용 공개 홈페이지입니다. GitHub Pages에 올리기 좋은 정적 사이트 구조입니다.

## 가장 먼저 수정할 파일

기본 정보는 여기서 바꾸면 됩니다.

```text
content/profile.json
```

예를 들어 이름, 소속, 이메일, GitHub 주소를 아래처럼 수정합니다.

```json
{
  "name": "Yoorim Son",
  "initials": "YS",
  "role": "Researcher",
  "affiliation": "Your University or Lab",
  "email": "your-email@example.com",
  "github": "https://github.com/your-id"
}
```

## 공개 내용 수정

- `content/profile.json`: 이름, 소개, 소속, 이메일, 링크
- `content/research.json`: About 페이지의 연구 관심사 카드
- `content/updates.json`: About 페이지의 Recent Updates
- `resume.html`: 학력, 경력, 스킬
- `papers.html`: 논문, preprint, manuscript
- `conferences.html`: 발표, 포스터
- `works.html`: 프로젝트, 데모, 공개 글
- `styles.css`: 보라색 테마, 글씨 크기, 간격

## 내부 연구 추적

외부에 보이면 안 되는 연구 추적은 `private/` 폴더에 적으면 됩니다.

`private/`는 `.gitignore`에 들어 있어서 GitHub에 올라가지 않습니다.

## 로컬에서 보기

```bash
npm run dev
```

브라우저에서 `http://127.0.0.1:4173`을 열면 됩니다.

내용이 안 바뀐 것처럼 보이면 브라우저에서 새로고침을 한 번 더 하거나 `Ctrl + F5`를 누르세요.

## 공유하기

추천은 GitHub Pages입니다.

```bash
git remote add origin https://github.com/YOUR_ID/YOUR_REPO.git
git add .
git commit -m "Create researcher homepage"
git push -u origin master
```

그다음 GitHub repository의 Settings > Pages에서 배포를 켜면 링크로 공유할 수 있습니다.
