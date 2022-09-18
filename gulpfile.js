// const gulp = require("gulp")

// const css = () => {
//     const postCSS = require("gulp-postcss");
//     const sass = require('gulp-sass')(require('sass'));
//     const minify = require("gulp-csso");
//     return gulp
//         .src("assets/scss/styles.scss")
//         .pipe(sass().on("error", sass.logError))
//         .pipe(postCSS([
//             require("tailwindcss"),
//             require("autoprefixer")
//         ]))
//         .pipe(minify())
//         .pipe(gulp.dest("static/css"));
// };

// exports.default = css;

var gulp = require('gulp');
var postcss = require('gulp-postcss');
var tailwindcss = require('tailwindcss');
var autoprefixer = require('autoprefixer');
var cssnano = require('cssnano');
var sass = require('gulp-sass')(require('sass'));

// Run:
// gulp sass
// Complies sass only once
gulp.task('sass', function () {
    var processors = [
        tailwindcss,
    ];
    return gulp.src('./scss/*.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(postcss(processors))
        .pipe(gulp.dest('./css'));
});

gulp.task('prod', function () {
    var processors = [
        tailwindcss,
        autoprefixer,
        cssnano
    ];
    return gulp.src('./scss/*.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(postcss(processors))
        .pipe(gulp.dest('./css'));
});

// Run:
// gulp watch
// Starts watcher and keeps compiling the css file as you make changes
gulp.task('watch', function () {
    gulp.watch("./**/*.scss", gulp.series('prod'));
});