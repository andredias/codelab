var gulp = require('gulp');
var stylus = require('gulp-stylus');
var autoprefixer = require('gulp-autoprefixer');
var comprimir = true;
var paths = {
    styles: [
        'server/static/styles/main.styl',
        'server/static/styles/menus.styl'
    ],
    dest: 'server/static/css'
};

gulp.task('stylus', function() {
    return gulp.src(paths.styles)
        .pipe(stylus({compress: comprimir}))
        .pipe(autoprefixer())
        .pipe(gulp.dest(paths.dest));
});

gulp.task('default', ['stylus']);
