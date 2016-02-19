var gulp = require("gulp");
var concat = require("gulp-concat");
var sass = require("gulp-sass");

gulp.task("default", function(){
  console.log("Starting");
  gulp.start("sass");
});

gulp.task("watch", function(){
  gulp.watch("sass/*.sass", ["sass"]);
})

gulp.task("sass", function(){
  return gulp.src("sass/*.sass")
    .pipe(sass())
    .pipe(concat("style.css"))
    .pipe(gulp.dest("website/static/css"))
});
