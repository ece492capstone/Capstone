var newsString = '';
var newsCounter = 0;
setInterval(myTimer, 2000);
setInterval(newsUpdateTime, 1800000);

function myTimer() {

    $.getJSON( "../newsfeed/outfile.json", function( data ) {
        var items = [];
        newsString = data;

    });

    if(newsCounter<newsString.length-1){
        newsCounter+=1;
    }
    else{
        newsCounter=0;
    }
    var currentNews = newsString[newsCounter];
    if(typeof(currentNews)!=='undefined' && currentNews.indexOf('Home Page')<0 ){
        document.getElementById("newsTitle").innerHTML = newsString[newsCounter];

    }
}

function newsUpdateTime() {

    $.getJSON( "../newsfeed/outfile.json", function( data ) {

        newsString = data;

    });

}