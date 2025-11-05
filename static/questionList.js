// function showScoreRangePopup() {
//     document.getElementById("scoreRangePopup").style.display = "block";
// }

// function hideScoreRangePopup() {
//     document.getElementById("scoreRangePopup").style.display = "none";
// }

// function selectScoreRange(range) {
//     var course_name_or_category = "{{ course_name_or_category }}";
//     var xhr = new XMLHttpRequest();
//     xhr.open("POST", courseQuestionScoreUrl, true);  // 使用传递的 URL
//     xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
//     xhr.onreadystatechange = function () {
//         if (xhr.readyState === 4 && xhr.status === 200) {
//             document.body.innerHTML = xhr.responseText;
//         }
//     };
//     xhr.send(JSON.stringify({
//         course_name_or_category: course_name_or_category,
//         score_range: range
//     }));
//     hideScoreRangePopup();
// }
