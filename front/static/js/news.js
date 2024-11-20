// 初期データを取得 (テンプレートから埋め込まれたデータを利用)
const newsItems = Array.from(document.querySelectorAll(".news-item")).map(item => {
  return {
    title: item.querySelector("h3").textContent,
    content: item.querySelector("p").textContent
  };
});

// ページあたりの項目数
const itemsPerPage = 5;

// ページの切り替え
function changePage(pageNumber) {
  const startIndex = (pageNumber - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const pageItems = newsItems.slice(startIndex, endIndex);

  const newsList = document.getElementById("your-news-list");
  newsList.innerHTML = ""; // コンテナをリセット

  pageItems.forEach(item => {
    const newsItem = document.createElement("div");
    newsItem.classList.add("news-item");
    newsItem.innerHTML = `<h3>${item.title}</h3><p>${item.content}</p>`;
    newsList.appendChild(newsItem);
  });
}

// 初期ページを表示
changePage(1);
