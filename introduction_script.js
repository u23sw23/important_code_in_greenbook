const stars = document.querySelectorAll('.stars span');
const score = document.querySelector('#score');
const ratingInput = document.querySelector('#rating');  // 获取隐藏的评分输入

stars.forEach((star, index) => {
    star.addEventListener('click', (e) => {
        const rect = star.getBoundingClientRect();
        const isLeft = e.clientX - rect.left < rect.width / 2;
        let rating = index + (isLeft ? 0.5 : 1);
        
        score.textContent = rating + 'stars';
        ratingInput.value = rating;  // 将评分保存到隐藏输入框
        
        stars.forEach((s, i) => {
            if (i < index) {
                s.style.setProperty('--v', '100');
            } else if (i === index) {
                s.style.setProperty('--v', isLeft ? '50' : '100');
            } else {
                s.style.setProperty('--v', '0');
            }
        });
    });
});