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

  const buttons = document.querySelectorAll('.pagination button');
  buttons.forEach(button => button.style.backgroundColor = '');
  buttons.forEach(button => button.style.color = '#111111');
  event.target.style.backgroundColor = '#EC7FB1';
  event.target.style.color = '#fff';
}


document.querySelector('.newsTab1').addEventListener('click', function() {
  const yourNewsList = document.querySelector('.your-news-list');
  const allNewsList = document.querySelector('.all-news-list');


  yourNewsList.style.display = 'none';
  allNewsList.style.display = 'flex';
  
  $('.newsTab1').css('background-color', '#EC7FB1');
  $('.newsTab1').css('color', '#fff');

  $('.youtab1').css('background-color', '#fff');
  $('.youtab1').css('color', '#EC7FB1');
});

document.querySelector('.youtab1').addEventListener('click', function() {
  const yourNewsList = document.querySelector('.your-news-list');
  const allNewsList = document.querySelector('.all-news-list');


  yourNewsList.style.display = 'block';
  allNewsList.style.display = 'none';

  $('.newsTab1').css('background-color', '#fff');
  $('.newsTab1').css('color', '#EC7FB1');

  $('.youtab1').css('background-color', '#EC7FB1');
  $('.youtab1').css('color', '#fff');
});


// 初期ページを表示
changePage(1);
