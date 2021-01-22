<template>
  <div style="max-height: 400px;">
    <input type="text" v-model="requestedTitle" label="Enter wiki page">
    <button @click="getData">Go</button>
    <div><h1>{{ title }}</h1></div>
    <div id=graph-container>

    </div>
  </div>
</template>

<script>
import Chart from 'chart.js';
import axios from 'axios';

export default {
  name: 'HelloWorld',
  data () {
    return {
      title: '',
      data: [],
      requestedTitle: 'Bitcoin'
    }
  },
  computed: {
    values() {
      return this.data.map(r => r.value)
    },
    labels() {
      return this.data.map(r => r.month + '-' + r.year)
    }
  },
  methods: {
    getData() {
      axios.get('http://localhost:5000/graph?title=' + this.requestedTitle)
        .then(res => {
          this.data = res.data.values
          this.title = res.data.title
        })
    },
    setup() {
      let container = document.getElementById('graph-container')
      if (container.hasChildNodes()) {
        container.removeChild(container.firstChild)
      }
      let canvas = document.createElement("canvas")
      canvas.id = "myChart"
      container.appendChild(canvas)
      console.log(container)

      var ctx = document.getElementById('myChart').getContext('2d');
      let myChart = new Chart(ctx, {
          type: 'line',
          data: {
              labels: this.labels,
              datasets: [{
                  label: 'Number of edits / month',
                  data: this.values,
                  borderWidth: 2
              }]
          },
          options: {
              scales: {
                  yAxes: [{
                      ticks: {
                          beginAtZero: true
                      }
                  }]
              }
          }
      });
      return myChart
    },
  },
  watch: {
    title() {
      this.setup()
    }
  }
}
</script>

<style scoped>

</style>
