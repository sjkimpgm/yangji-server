<template>
  <div id="app">
    <el-container direction="horizontal">
      <el-aside width="200px">
        <el-menu :default-openeds="['1', '3']" :router="true">
          <el-menu-item index="/measurement_table">
            <i class="el-icon-document"></i>
            <span>계측값 표로 보기</span>
          </el-menu-item>
          <el-menu-item index="/measurement_graph">
            <i class="el-icon-data-line"></i>
            <span>계측값 그래프로 보기</span>
          </el-menu-item>
          <el-menu-item index="/measurement_3d">
            <i class="el-icon-video-camera"></i>
            <span>계측값 3D로 보기</span>
          </el-menu-item>
          <el-menu-item index="/device">
            <i class="el-icon-set-up"></i>
            <span>기기 관리</span>
          </el-menu-item>
          <el-menu-item index="5">
            <i class="el-icon-setting"></i>
            <span>설정</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-main><router-view /></el-main>
    </el-container>
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
