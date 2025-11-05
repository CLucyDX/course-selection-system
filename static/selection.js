function scoreRangeVisibility() {
    var courseSelector = document.getElementById('course-selector');
    var scoreRange = document.getElementById('score-range');
    if (courseSelector.value === 'LLM_score') {
        scoreRange.style.display = 'block';
    } else {
        scoreRange.style.display = 'none';
    }
}
$(document).ready(function(){

    // 确保初始状态正确
    scoreRangeVisibility();

    // 监听 id 为 course-selector 的元素（可能是下拉框）的值变化,绑定 change 事件处理函数
    $('#course-selector').change(function() { 
        // clear 
        $('#result-list').empty();
        // 调用，确保状态正确
        scoreRangeVisibility();

        // 当值变化且不等于 'select' 时，发送 AJAX GET 请求到 /display_courses 路径，并带上当前的值作为 type 参数
        var type = $(this).val();  
        if (type !== 'select') {  
            if(type === 'course_name'){
                $.ajax({  
                    url: '/courseList',  
                    type: 'GET',  
                    data: { type: type },  
                    success: function(data) {  
                        var html = '<ul>';  
                        $.each(data, function(index, item) {  
                            var linkText = item.name || item.category;  
                            html += '<li><a href="/course/' + encodeURIComponent(linkText) + '">' + linkText + '</a></li>';  
                        });  
                        html += '</ul>';  
                        $('#result-list').html(html);  
                    },  
                    error: function(error) {  
                        console.log(error);  
                    }  
                }); 
            }
            if(type === 'course_category'){
                $.ajax({  
                    url: '/categoryList',  
                    type: 'GET',  
                    data: { type: type },  
                    success: function(data) {  
                        var html = '<ul>';  
                        $.each(data, function(index, item) {  
                            var linkText = item.name || item.category;  
                            html += '<li><a href="/category/' + encodeURIComponent(linkText) + '">' + linkText + '</a></li>';  
                        });  
                        html += '</ul>';  
                        $('#result-list').html(html);  
                    },  
                    error: function(error) {  
                        console.log(error);  
                    }  
                }); 
            }
            if(type === 'LLM_score'){
                scoreRangeVisibility();
                $('#score-range').change(function() {
                    var type = $(this).val(); 
                    $.ajax({  
                        url: '/scoreRangeQ',  
                        type: 'GET',  
                        data: { type: type },  
                        success: function(data) {  
                            var html = '<ul>';  
                            $.each(data.results, function(index, item) {  
                                linkText = item.llm_id;
                                html += '<li><a href="/score/' + encodeURIComponent(linkText) + '">' + item.q_text + ' - ' + item.score + ' - ' + item.llm_id + '</a></li><br>'; 
                            });  
                            html += '</ul>';  
                            $('#result-list').html(html);  
                        },  
                        error: function(error) {  
                            console.log(error);  
                        }  
                    });
                });
            }
        }  
    });
});