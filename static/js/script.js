console.log("script.js");

function datejapanese (pubdate) {
    const date = new Date(pubdate);
    const pubdateTxt = date.getFullYear()+ "年"
        + (date.getMonth()+1)+"月"
        + date.getDate()+ "日 "
        + date.getHours()+ "時"
        + date.getMinutes()+ "分"
        + date.getSeconds()+ "秒";
        return pubdateTxt;
    }



