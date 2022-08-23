window.addEventListener("load", function () {
    $("#submit").on("click", function() { submit();});

    //setInterval 指定したミリ秒だけ待って何回でも実行する
    // setInterval(refresh, 1000);

    //setTimeoutは指定したミリ秒だけ待って1回だけ実行する。
    //setTimeout(refresh, 1000);

    //ロングポーリングの場合、Ajaxが終わってから再度送信を行うため、setIntervalではなくsetTimeoutを使う。
    refresh();
});

function submit() {
    let form_elem = "#form_area";

    let data = new FormData( $(form_elem).get(0));
    let url = $(form_elem).prop("action");
    let method = $(form_elem).prop("method");

    $.ajax({
        url: url,
        type: method,
        data: data,
        processData: false,
        contentType: false,
        dataType: 'json' //レスポンスは必ずjsonで返す
    }).done( function(data, status, xhr) {
        if (data.error) {
            console.log("ERROR");
            console.log("data.error通っている");
        } else {
            $("#content_area").html(data.content);
            console.log("data.errorなし、成功" + data.content);
            $("#textarea").val("");
        }
    }).fail ( function(xhr, status, error) {
        console.log(status + ":" + error);
        console.log("failを通っている");
    });

}

function refresh() {

    //ここで最新の投稿内容のIDを取得。クエリストリングを作る
    // ?first=1
    // request.GET["first"]
    let param = "?" + $("#first").prop("name") + "=" + $("#first").val();
    // console.log(param);
    
    $.ajax({
        url: REFRESH_URL + param,
        type: "GET",
        dataType: "json"
    }).done( function(data, status, xhr) {
        if (!data.error) {
            $("#content_area").html(data.content);
        }
    }).fail( function(xhr, status, error) {
        console.log(status + ":" + error);
    }).always( function() {
        //このAjaxが終了次第、一定時間待って再実行する。
        setTimeout(refresh, 500);
        // console.log("refresh再開");
    });
}