// 图片
function openImage(imageUrl) {
    window.open(imageUrl, '_blank');
}

// 保存
$(document).ready(function() {
    // 添加点击事件处理函数，用于保存相关数据到本地文件
    $('.save-button').click(function() {
        var qText = $(this).data('qtext');
        var qCateg = $(this).data('qcateg');
        var courseName = $(this).data('coursename');
        var answerImg = $(this).data('answerimg');
        var score = $(this).data('score');
        var comments = $(this).data('comments');

        // 构造要保存的文本内容
        var textContent = "Question Text: " + qText + "\n";
        textContent += "Question Category: " + qCateg + "\n";
        textContent += "Course Name: " + courseName + "\n";
        textContent += "Score: " + score + "\n";
        textContent += "Comments: " + comments;

        


        // 创建一个 Blob 对象并下载
        var blob = new Blob([textContent], { type: "text/plain;charset=utf-8" });
        saveAs(blob, "question_detail.txt");
    });
});