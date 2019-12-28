let hitNumber = 2; //検索にヒットしたアーティストの数

//
// class artistInfomation {
//   constructor(artistName, musicality, fanBase) {
//     this.artistName = artistName;
//     this.musicality = artistName;
//     this.fanBase = fanBase;
//   }
// }

$(function() {
  //ページを読み込んだ後に実行

  createResult();
});

const createResult = () => {
  //検索結果の表示
  for (var i = 0; i < hitNumber; i++) {
    // div要素を生成
    var div = document.createElement("div");
    // div要素のclassを追加
    div.className = "resultFrom";
    // p要素を生成
    var name = document.createElement("h1");
    var music = document.createElement("h3");
    var fan = document.createElement("h3");

    // アーティスト名
    name.className = "artistName";
    name.textContent = "Name" + (i + 1);
    //音楽性
    music.className = "musicality";
    music.textContent = "音楽性";
    //ファン増
    fan.className = "fanBase";
    fan.textContent = "ファン層";

    // p要素をdiv要素の子要素に追加
    div.appendChild(name);
    div.appendChild(music);
    div.appendChild(fan);

    //お気に入りボタンの生成・追加
    var favorite = document.createElement("button");
    favorite.className = "favoriteButton";
    favorite.textContent = "お気に入り★";
    favorite.value = i;
    div.appendChild(favorite);

    // 生成したdiv要素を追加する
    document.getElementById("formList").appendChild(div);
  }
};
