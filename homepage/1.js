function showSelectedOptions() {
    event.preventDefault(); // 阻止表单默认提交（如果按钮类型为submit的话）
    var radios = document.querySelectorAll('input[type="radio"]:checked');
    document.getElementById('selectedOptions').innerHTML = '<h3>选中的选项:</h3><ul>';
    radios.forEach(function(radio) {
        document.getElementById('selectedOptions').innerHTML += '<li>' + radio.value + '</li>';
    });
    document.getElementById('selectedOptions').innerHTML += '</ul>';
}

// 如果希望在页面加载时就绑定这个函数到按钮上，也可以在 DOMContentLoaded 事件内进行
document.addEventListener('DOMContentLoaded', function() {
    // 这里可以进一步做其他初始化操作
});