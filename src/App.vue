<template>
  <div id="app">
    <v-app>
      <v-navigation-drawer 
        stateless
        permanent
        app
      >
        <v-list>
          <v-list-item to="/measurement_table" link>
            <v-list-item-action>
              <v-icon>table_chart</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>표로 보기</v-list-item-title>
            </v-list-item-content>
          </v-list-item>

          <v-list-item to="/measurement_table_day">
            <v-list-item-action>
              <v-icon>table_chart</v-icon>
            </v-list-item-action>
            <v-list-item-title>일별 보기</v-list-item-title>
          </v-list-item>

          <v-list-item to="/measurement_table_realtime">
            <v-list-item-action>
              <v-icon>table_chart</v-icon>
            </v-list-item-action>
            <v-list-item-title>실시간 표로 보기</v-list-item-title>
          </v-list-item>
        
          <v-list-item to="/measurement_graph">
            <v-list-item-action>
              <v-icon>insert_chart</v-icon>
            </v-list-item-action>
            <v-list-item-title>그래프로 보기</v-list-item-title>
          </v-list-item>

          <v-list-item to="/measurement_graph_realtime">
            <v-list-item-action>
              <v-icon>insert_chart</v-icon>
            </v-list-item-action>
            <v-list-item-title>실시간 그래프로 보기</v-list-item-title>
          </v-list-item>

          <v-list-item to="measurement_3d">
            <v-list-item-action>
              <v-icon>layers</v-icon>
            </v-list-item-action>
            <v-list-item-title>3D로 보기</v-list-item-title>
          </v-list-item>
        
          <v-list-item to="device_setup">
            <v-list-item-action>
              <v-icon>location_on</v-icon>
            </v-list-item-action>
            <v-list-item-title>기기 관리</v-list-item-title>
          </v-list-item>

          <v-list-item>
            <v-list-item-action>
              <v-icon>settings</v-icon>
            </v-list-item-action>
            <v-list-item-title>설정</v-list-item-title>
          </v-list-item>
        </v-list>
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
