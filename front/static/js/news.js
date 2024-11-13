// ダミーデータ
const newsItems = [
    { title: "ニュース1", content: "内容1" },
    { title: "ニュース2", content: "内容2" },
    { title: "ニュース3", content: "内容3" },
    { title: "ニュース4", content: "内容4" },
    { title: "ニュース5", content: "内容5" },
    { title: "ニュース6", content: "内容6" },
    { title: "ニュース7", content: "内容7" },
    { title: "ニュース8", content: "内容8" },
    { title: "ニュース9", content: "内容9" },
    { title: "ニュース10", content: "内容10" },
    // 続く...
  ];
  
  const itemsPerPage = 5;
  
  // ページの切り替え
  function changePage(pageNumber) {
    const startIndex = (pageNumber - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const pageItems = newsItems.slice(startIndex, endIndex);
  
    const newsList = document.getElementById("news-list");
    newsList.innerHTML = "";
  
    pageItems.forEach(item => {
      const newsItem = document.createElement("div");
      newsItem.classList.add("news-item");
      newsItem.innerHTML = `<h3>${item.title}</h3><p>${item.content}</p>`;
      newsList.appendChild(newsItem);
    });
  }
  
  // 初期ページを表示
  changePage(1);
  