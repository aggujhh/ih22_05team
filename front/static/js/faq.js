console.log("faq.js")

const content_list = []
const content = document.querySelector(".content")
window.addEventListener("load", () => {

    content_list.push(content.innerHTML)
    content_list.push(`
            <h3><i class="icon"></i>ご依頼について</h3>
            <div class="faq-item">
                <h3><i class="icon"></i>お仕事を依頼・募集するにはどうしたらいいですか？</h3>
                <p>メニューの「依頼する」ボタンを押し、依頼したい内容を作成した後に募集・相談することが可能になります。</p>
            </div>
            <div class="faq-item">
                <h3><i class="icon"></i>お仕事の依頼・募集時にイメージ画像を添付することは可能ですか？</h3>
                <p>添付は可能にしておりますが、2次転載・利用可能かどうかを確認した上での掲載をお願い致します。</p>
            </div>
    `)
    content_list.push(`
            <h3><i class="icon"></i>お支払いについて</h3>
            <div class="faq-item">
                <h3><i class="icon"></i>代金はいつどこに支払えばいいですか？</h3>
                <p>お支払いの方法はPayPal(ペイパル)決済、クレジットカード決済、銀行振込のどれかとなります。成約後7日以内にお支払いください。振込の場合は下記が振込先情報になります。
                <br><small>※クレジットカード決済はVisa・MasterCard・American Express・JCB・Diners Club・Discoverの6種に対応しています。</small><br>
                ==========<br>
                銀行名: 楽天銀行<br>
                支店名: 第二営業支店<br>
                種類: 普通預金<br>
                口座番号: 7631664<br>
                口座名義: 株式会社 オタクラウド<br>
                ==========</p>
            </div>
            <div class="faq-item">
                <h3><i class="icon"></i>楽天銀行の口座を持っていませんが銀行振込は可能ですか？</h3>
                <p>可能です。振込先銀行が楽天銀行となっているだけで、ご契約されている銀行から銀行振り込みが可能です。</p>
            </div>
    `)
    content_list.push(`
            <h3><i class="icon"></i>制作、発送について</h3>
            <div class="faq-item">
                <h3><i class="icon"></i>商品が届かない場合はどうしたらいいですか？</h3>
                <p>制作者から配送追跡番号を共有してもらい、商品の配送情報を確認してください。</p>
            </div>
            <div class="faq-item">
                <h3><i class="icon"></i>途中で制作者からの連絡が途絶えたらどうしたらいいですか？</h3>
                <p>当サービス側からも制作者に返信を行うように促すので、一度その旨をお問い合わせフォームよりご連絡ください。</p>
            </div>
    `)
    content_list.push(`
            <h3><i class="icon"></i>返品交換について</h3>
            <div class="faq-item">
                <h3><i class="icon"></i>商品を返品したい場合はどうしたらいいですか？</h3>
                <p>基本的に成約及び納品後の返品は不可ですが、制作者との合意のもとであれば可能です。その場合、成約した成約フォームの「検品・制作者評価」ボタンは押さず、お問い合わせフォームより返品の旨のご連絡をいただけましたら対応致します。</p>
            </div>
    `)
    content_list.push(`
            <h3><i class="icon"></i>その他質問</h3>
            <div class="faq-item">
                <h3><i class="icon"></i>確定申告を行う必要はありますか？</h3>
                <p>お手数ですが、お問い合わせフォームからその旨ご連絡ください。個別に対応致します。</p>
            </div>
            <div class="faq-item">
                <h3><i class="icon"></i>本人確認登録後、苗字や住所等が変わった場合はどうしたら良いですか？</h3>
                <p>当サービス側からも制作者に返信を行うように促すので、一度その旨をお問い合わせフォームよりご連絡ください。</p>
            </div>
    `)
    faq_change()
})


function faq_change() {
    const sidebars = document.querySelectorAll(".sidebar li")
    console.log(sidebars)
    sidebars.forEach((sidebar, i) => {
        sidebar.addEventListener("click", () => {
            sidebars.forEach((e) => {
                e.classList.remove("active")
            })
            sidebar.classList.add("active")
            content.innerHTML = content_list[i]
        })
    })
}