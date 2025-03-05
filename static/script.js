// script.js
// document.addEventListener('DOMContentLoaded', function () {
//     const watermark = document.createElement('div');
//     watermark.className = 'watermark';
//     watermark.textContent = 'Dynamic Watermark';
//     document.body.appendChild(watermark);
// });

// JavaScript 函数：根据选择的类型动态控制时间输入框
function toggleTimeInput(selectElement) {
    // 获取当前行的输入框
    const timeInput = selectElement.parentElement.parentElement.querySelector('input[type="text"]');
    // 如果选择的是 "禁止使用"，则禁用输入框并清空值
    if (selectElement.value === 'Forbidden') {
        timeInput.disabled = true;
        timeInput.value = ''; // 清空时间
    } else {
        // 否则启用输入框
        timeInput.disabled = false;
    }
}

function updateClock() {
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const seconds = now.getSeconds().toString().padStart(2, '0');
    const timeString = `${hours}:${minutes}:${seconds}`;
    document.getElementById('clock').textContent = timeString;
    const month = (now.getMonth() + 1).toString().padStart(2, '0');
    const day = now.getDate().toString().padStart(2, '0');
    const year = now.getFullYear();
    const dateString = `${year}-${month}-${day}`;
    document.getElementById('date').textContent = dateString;
}

setInterval(updateClock, 1000); // 更新时钟每秒
updateClock(); // 初始化时钟


// function generateWatermark(text) {
//     const container = document.getElementById("watermark");
//     const cols = Math.ceil(window.innerWidth / 200);
//     const rows = Math.ceil(window.innerHeight / 100);
//     for (let i = 0; i < rows; i++) {
//         for (let j = 0; j < cols; j++) {
//             let watermark = document.createElement("div");
//             watermark.className = "watermark";
//             watermark.style.top = `${i * 100}px`;
//             watermark.style.left = `${j * 200}px`;
//             watermark.innerText = text;
//             container.appendChild(watermark);
//         }
//     }
// }

generateWatermark("原创设计 - 保持版权");