<template>
  <div class="stats">
    <div class="left-side">
      <div class="player-info">
        <img :src="stats.avatar_url" class="player-avatar" />
        <div class="player-details">
          <h1 class="player-name">{{ stats.username }}</h1>
          <div class="player-country">
            <span>{{ stats.country.name }}</span>
          </div>
        </div>
      </div>
      <div class="player-stats">
        <div class="player-pp">
          <span class="pp-value">{{ stats.statistics.pp }}</span>
          <span class="pp-label">pp</span>
        </div>
        <div class="player-accuracy">
          <span class="accuracy-value">{{ stats.statistics.hit_accuracy }}</span>
          <span class="accuracy-label">Accuracy</span>
        </div>
      </div>
    </div>
    <div class="right-side">
      <div class="playcount-graph">
        <!-- Playcount graph goes here -->
        <canvas ref="ppChart"></canvas>
      </div>
      <div class="suggestions">
        <!-- Text suggestions go here -->
      </div>
      <div class="maps">
        <!-- Map suggestions go here -->
      </div>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';
import 'chartjs-adapter-date-fns';
import { enUS } from 'date-fns/locale';

export default {
  props: {
    stats: {
      type: Object,
      required: true,
    },
  },
  mounted() {
    this.fetchScores();
  },
  methods: {
    async fetchScores() {
      const response = await fetch(`http://localhost:8000/api/user/${this.stats.id}/scores`);
      const scores = await response.json();

      // Sort scores by date and pp
      scores.sort((a, b) => {
        const dateA = new Date(a.created_at);
        const dateB = new Date(b.created_at);
        const ppA = a.pp;
        const ppB = b.pp;
        if (dateA > dateB) return 1;
        if (dateA < dateB) return -1;
        if (ppA > ppB) return -1;
        if (ppA < ppB) return 1;
        return 0;
      });

      // Create array of data points for each score
      const data = scores.map((score) => ({
        x: new Date(score.created_at),
        y: score.pp,
        name: score.beatmap.name,
        link: score.beatmap.link,
      }));

      // Create array of best scores of each day
      const bestScoresByDay = scores.reduce((accumulator, score) => {
        const date = new Date(score.created_at).toDateString();
        if (!accumulator[date] || accumulator[date].pp < score.pp) {
          accumulator[date] = {
            pp: score.pp,
            name: score.beatmap.name,
            link: score.beatmap.link,
            date: new Date(score.created_at),
          };
        }
        return accumulator;
      }, {});

      // Create array of performance line points
      const performanceLine = Object.values(bestScoresByDay).sort((a, b) => {
        const dateA = a.date;
        const dateB = b.date;
        const ppA = a.pp;
        const ppB = b.pp;
        if (dateA > dateB) return 1;
        if (dateA < dateB) return -1;
        if (ppA > ppB) return -1;
        if (ppA < ppB) return 1;
        return 0;
      }).map((score, i, arr) => {
        const { date, pp } = score;
        if (i === 0 || i === arr.length - 1) {
          return { x: date, y: pp };
        }
        const prev = arr[i - 1];
        const next = arr[i + 1];
        const dx1 = (date - prev.date) / 3;
        const dy1 = (pp - prev.pp) / 3;
        const dx2 = (next.date - date) / 3;
        const dy2 = (next.pp - pp) / 3;
        return {
          x: date,
          y: pp,
          cp1x: date - dx1,
          cp1y: pp - dy1,
          cp2x: date + dx2,
          cp2y: pp + dy2,
        };
      });

      const ctx = this.$refs.ppChart.getContext('2d');
      new Chart(ctx, {
        type: 'line',
        data: {
          datasets: [
            {
              label: 'Performance',
              data: data,
              backgroundColor: 'rgba(0, 151, 167, 0.2)',
              borderColor: 'rgba(0, 151, 167, 0)',
              borderWidth: 2,
              pointRadius:

                6,
              pointBackgroundColor: 'rgba(0, 151, 167, 0.7)',
              pointHoverRadius: 5,
              pointHoverBackgroundColor: 'rgba(0, 151, 167, 1)',
              pointHoverBorderColor: 'rgba(0, 151, 167, 1)',
            },
            {
              label: 'Performance Line',
              data: performanceLine,
              backgroundColor: 'rgba(0, 0, 0, 0.05)',
              borderColor: 'rgba(0, 0, 0, 0.5)',
              borderWidth: 2,
              pointRadius: 0,
              lineTension: 0.4,
              borderCapStyle: 'line',
              fill: {
                target: 'origin',
                above: 'rgba(0, 0, 0, 0.05)',
                below: 'rgba(0, 0, 0, 0.1)',
              },
              cubicInterpolationMode: 'monotone',
            },
          ],
        },
        options: {
          scales: {
            x: {
              type: 'time',
              time: {
                displayFormats: {
                  day: 'MMM D',
                },
                locale: enUS,
              },
              ticks: {
                autoSkip: true,
                maxTicksLimit: 20,
              },
            },
            y: {
              title: {
                display: true,
                text: 'PP',
              },
              ticks: {
                beginAtZero: true,
              },
            },
          },
          plugins: {
            tooltip: {
              callbacks: {
                label: (context) => {
                  const score = context.dataset.data[context.dataIndex];
                  return `${score.name} - ${score.y} pp`;
                },
                title: (context) => {
                  const score = context[0].dataset.data[context[0].dataIndex];
                  return new Date(score.x).toLocaleDateString(enUS, {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric',
                  });
                },
              },
            },
            legend: {
              display: true,
              position: 'bottom',
            },
          },
        },
      });
    },
  },
};
</script>






<style>
.playcount-graph {
  width: 100%;
  max-width: 800px;
  margin: auto;
}

.stats {
  display: flex;
  flex-wrap: wrap;
  padding: 2rem;
}

.left-side {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 25rem;
  margin-right: 2rem;
}

.player-info {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.player-avatar {
  width: 6rem;
  height: 6rem;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 1rem;
}

.player-details {
  display: flex;
  flex-direction: column;
}

.player-name {
  font-size: 2rem;
  margin: 0;
}

.player-country {
  display: flex;
  align-items: center;
}

.player-country img {
  margin-right: 0.5rem;
}

.player-stats {
  display: flex;
  flex-direction: column;
}

.player-pp,
.player-accuracy {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
}

.pp-value,
.accuracy-value {
  font-size: 2.5rem;
  margin-right: 0.5rem;
}

.pp-label,
.accuracy-label {
  font-size: 1.5rem;
  color: #666;
}

.right-side {
  flex: 1;
}

.playcount-graph,
.suggestions,
.maps {
  margin-bottom: 2rem;
}

.playcount-graph {
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
  padding: 1rem;
}

.suggestions {
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
  padding: 1rem;
}

.maps {
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
  padding: 1rem;
}
</style>