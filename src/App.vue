<template>
  <div id="app">
    <v-app>
      <v-navigation-drawer 
        stateless
        permanent
        app
      >
        <v-list-tile to="/measurement_table">
          <v-list-tile-action>
            <v-icon>table_chart</v-icon>
          </v-list-tile-action>
          <v-list-tile-title>계측값 표로 보기</v-list-tile-title>
        </v-list-tile>

        <v-list-tile to="/measurement_table_day">
          <v-list-tile-action>
            <v-icon>table_chart</v-icon>
          </v-list-tile-action>
          <v-list-tile-title>계측값 일별 보기</v-list-tile-title>
        </v-list-tile>
        
        <v-list-tile to="/measurement_graph">
          <v-list-tile-action>
            <v-icon>insert_chart</v-icon>
          </v-list-tile-action>
          <v-list-tile-title>계측값 그래프로 보기</v-list-tile-title>
        </v-list-tile>

        <v-list-tile to="measurement_3d">
          <v-list-tile-action>
            <v-icon>layers</v-icon>
          </v-list-tile-action>
          <v-list-tile-title>계측값 3D로 보기</v-list-tile-title>
        </v-list-tile>
        
        <v-list-tile to="device_setup">
          <v-list-tile-action>
            <v-icon>location_on</v-icon>
          </v-list-tile-action>
          <v-list-tile-title>기기 관리</v-list-tile-title>
        </v-list-tile>

        <v-list-tile to="change_measurement">
          <v-list-tile-action>
            <v-icon>location_on</v-icon>
          </v-list-tile-action>
          <v-list-tile-title>측정값 변환</v-list-tile-title>
        </v-list-tile>

        <v-list-tile>
          <v-list-tile-action>
            <v-icon>settings</v-icon>
          </v-list-tile-action>
          <v-list-tile-title>설정</v-list-tile-title>
        </v-list-tile>
      </v-navigation-drawer>
      <v-content>
        <v-container fluid>
          <router-view></router-view>
        </v-container>
      </v-content>
    </v-app>
  </div>
</template>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
