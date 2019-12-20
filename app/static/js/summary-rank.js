// ドーナッツチャート用の配色データ
const materialColors1 = ['#80CBC4', '#FFF59D', '#EF9A9A', '#9FA8DA', '#A5D6A7', '#FFE082', '#F48FB1', '#90CAF9', '#C5E1A5', '#FFCC80', '#CE93D8', '#81D4FA', '#E6EE9C', '#FFAB91', '#B39DDB', '#80DEEA',];
const materialColors2 = ['#00897B', '#FDD835', '#E53935', '#3949AB', '#43A047', '#FFB300', '#D81B60', '#1E88E5', '#7CB342', '#FB8C00', '#8E24AA', '#039BE5', '#C0CA33', '#F4511E', '#5E35B1', '#00ACC1',];

// 収入支出のランキンググラフを描写する関数
const setRankChart = () => {
    // 収入データ取得リクエスト
    fetch(`/api/incomerank`).then(response => {
        response.json().then((data) => {
            // HTTP通信によりJSONデータを取得
            // Chart.jsにデータを渡す設定
            const ctx = document.getElementById('incomeReport').getContext('2d');
            const chart = new Chart(ctx, {
                type: 'doughnut',   // ドーナッツチャートを選択
                data: {
                    labels: data.labels,   // 取得したラベルテキスト
                    datasets: [{
                            label: '# 収入',
                            data: data.values,    // 取得したデータ
                            backgroundColor: materialColors1 // 配色データ
                        }]
                },
                options: {
                    legend: {
                        position: 'right'   // データのラベル表示位置
                    }
                }
            });
        });
    });
    // 支出データ取得リクエスト
    fetch(`/api/expensesrank`).then(response => {
        response.json().then((data) => {
            const ctx = document.getElementById('expensesReport').getContext('2d');
            const chart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: data.labels,
                    datasets: [{
                            label: '# 支出',
                            data: data.values,
                            backgroundColor: materialColors2
                        }]
                },
                options: {
                    legend: {
                        position: 'right'
                    }
                }
            });
        });
    });
};

(() => {
    // 収支ランキング表示
    setRankChart();
})();