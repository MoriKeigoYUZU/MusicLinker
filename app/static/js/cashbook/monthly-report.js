// 月ごとの日別集計グラフ表示処理
const setMonthlyReport = (targetYM) => {

    var targetYM = (targetYM !== undefined) ? targetYM : dayjs().format('YYYYMM');

    fetch(`/api/monthlyreport/${targetYM}`).then(response => {
        response.json().then((data) => {
            const ctx = document.getElementById('monthlyReport').getContext('2d');
            const myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [
                        {
                            type: 'bar',
                            label: '収入',
                            data: data.chartIncome,
                            borderColor: 'hsla(211, 100%, 65%, 0.8)',
                            backgroundColor: 'hsla(211, 100%, 65%, 0.5)',
                        },
                        {
                            type: 'bar',
                            label: '支出',
                            data: data.chartExpenses,
                            borderColor: 'hsla(355, 100%, 78%, 0.8)',
                            backgroundColor: 'hsla(355, 100%, 78%, 0.5)',
                        },
                        {
                            type: 'line',
                            label: '積み上げ残高',
                            data: data.chartAmount,
                            borderColor: 'hsla(134, 41%, 61%, 0.8)',
                            pointBackgroundColor: 'hsla(134, 41%, 61%, 0.5)',
                            fill: false,
                        },
                    ],
                },
                options: {
                    responsive: true
                }
            });
        });
    });
};

// 年月変更の処理を定義
const monthlyReportTargetChanged = (elm) => {
    var index = elm.selectedIndex;
    var value = elm.options[index].value;
    setMonthlyReport(value);
};

const monthlyReportInit = () => {
    selectYm = document.getElementById('form-monthly-select-ym');
    let mstart = dayjs().set('day', 1);
    console.log(mstart.format());
    for (let i = 0; i < 12; i++) {
        let opt = document.createElement('option');
        if (i === 0) opt.selected = true;
        opt.value = mstart.format('YYYYMM');
        opt.text = mstart.format('YYYY年MM月');
        selectYm.appendChild(opt);

        // 1ヶ月前にする
        mstart = mstart.add(-1, 'month');
    }

    // 月ごと日別データ表示
    setMonthlyReport();

    // 年月選択が変更されたイベントの処理を定義
    document.querySelector('#form-monthly-select-ym').addEventListener('change', function (ev) {
        monthlyReportTargetChanged(this);
    });
};


(() => {
    monthlyReportInit();
})();