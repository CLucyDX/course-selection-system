var icon = document.querySelector('.dropdown-icon');
var menu = document.querySelector('.dropdown-menu');

var assignments_list = {{ assignments_list|tojson|safe }}; // 将后端传来的问题列表转换为 JavaScript 对象
var course_names = {{ course_names|tojson|safe }};
icon.addEventListener('click', function() {
    if (menu.style.display === 'block') {
        menu.style.display = 'none';
    } else {
        menu.style.display = 'block';
    }
});

$(document).ready(function(){
    $('#a').on('input', function(){
        var searchTerm = $(this).val();
        updateList(searchTerm);
    });

    $('.search_box').mouseenter(function() {
        $('.a').css('width', '300px');
        $('#b_results').show();
    }).mouseleave(function() {
        var searchTerm = $('#a').val();
        if (searchTerm.trim() === '') {
            $('.a').css('width', '0');
            $('#b_results').hide();
        }
        else{
            $('.a').css('width', '300px');
            $('#b_results').show();
        }
    });
});
function updateList(searchTerm) {
    $('#b_results').empty();
    $('#b_results').append('<ul>');
    $('#b_results ul').css('list-style-type', 'none');
    var count = 0; // 计数器，用于限制显示数量
    if (searchTerm.trim() !== '') { // 检查搜索框中是否有内容
        $('.a').css('width', '300px'); // 如果有内容，设置搜索框宽度为300px
    } 
    $.each(course_names, function(index, course_name){
        if (course_name.course_name.toLowerCase().includes(searchTerm.toLowerCase())){
            if (count < 5) { // 这里显示10个内容
                $('#b_results ul').append('<li class="b_item">' + course_name.course_name + '</li>');
                count++;
            }
        }
    });
    $.each(assignments_list, function(index, assignments){
        if (assignments.q_text.toLowerCase().includes(searchTerm.toLowerCase())){
            if (count < 5) { // 这里显示10个内容
                $('#b_results ul').append('<li class="b_item">' + assignments.q_text + '</li>');
                count++;
            }
        }
    });
    $('#b_results').append('</ul>');
}
$(document).on('click', '.b_item', function(){
    var selectedQuestion = $(this).text();
    $('#a').val(selectedQuestion); 
    $('#b_results').empty(); 
});
function submitSearch() {
    document.getElementById("search_form").submit();
}