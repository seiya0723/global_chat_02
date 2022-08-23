// Cookieの中からCSRFトークンを取り出し、Ajax送信前にCSRFトークンをセットするJavaScript
function getCookie(name) {
    var cookieValue = null;

    //ブラウザのCookieを参照する(document.cookie)。中身が有る場合のみ処理を実行する
    if (document.cookie && document.cookie !== '') {

        //Cookieは文字列なので、;で区切って配列にする(後で値を取れるようにするため)
        // [ "aaa=AAA", "bbb=BBB", "ccc=CCC", "csrftoken=XXXXXXXXXXXXXXX" ]

        var cookies = document.cookie.split(';');

        /*
        for (let cookie of cookies){
            console.log(cookie);
        }
        */

        for (var i = 0; i < cookies.length; i++) {

            //両端の空白を除去する(文字列の長さを考慮するため)
            var cookie = cookies[i].trim();

            //name(今回はcsrftoken)に対応する値を取り出す。

            // Does this cookie string begin with the name we want?
            // csrftoken=が一致する場合
            if (cookie.substring(0, name.length + 1) === (name + '=')) {

                //decodeURIComponent()でパーセントエンコードされた文字列、クエリパラメータを普通の文字列に直す      //CSRFの値からスタート
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }


    }
    return cookieValue;
}
//文字列型でCookieからCSRFトークンの値を抜き取る
var csrftoken = getCookie('csrftoken');

/*
127.0.0.1:8000
document.cookieの中身

aaa=AAA;bbb=BBB;ccc=CCC;csrftoken=XXXXXXXXXXXXXXX;
*/




//POSTリクエストを送信する時はDjangoのセキュリティ対策が発動するので、CSRFトークンが必要。そうしないと401 Forbiddenエラーになる。
//Ajaxも同様でAjaxのPOSTリクエストを送信する時も、CSRFトークンをセットしなければならない。

//Ajaxを送信する直前に、CSRFトークンをリクエストのヘッダにセットする。(ただし、GET|HEAD|OPTIONS|TRACEのいずれかの場合はCSRFトークンはセットしない)



function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    //正規表現が含むかどうかチェック
    //https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Global_Objects/RegExp/test
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}



// $.ajax()を実行する時、その前に$.ajaxSetup()が発動する
$.ajaxSetup({
    
    beforeSend: function(xhr, settings) {
        // settingsは$.ajaxのオブジェクト型の引数が入る。settings.typeでAjax送信時のメソッドが取れる
        // GET,HEAD,OPTIONS,TRACEのメソッドではないことをチェックする
        // this.crossDomainは別サイトに対して送信する場合trueが返却される

        // console.log(settings);
        // console.log(settings.type);

        // GET,HEAD,OPTIONS,TRACEのメソッドではない かつ 別サイトに送信されるAjaxではない
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {

            //AjaxのリクエストヘッダにCSRFトークンをセットする(POST(PUT,DELETE,PATCH)メソッドの時だけ送信する(GET,HEAD,OPTIONS,TRACEのメソッドの場合はCSRFトークンを送信しない))
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
