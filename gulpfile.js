var gulp = require('gulp');
var stylus = require('gulp-stylus');
var autoprefixer = require('gulp-autoprefixer');
var stylus_normalize = require('stylus-normalize');
var elf_grid = require('elf-grid');
var rupture = require('rupture');
var watch = require('gulp-watch');
var comprimir = true;
var paths = {
    styles: [
        'server/static/styles/main.styl',
        'server/static/styles/menus.styl',
        'server/static/styles/headers_footers.styl'
    ],
    dest: 'server/static/css'
};

gulp.task('stylus', function() {
    return gulp.src(paths.styles)
        .pipe(stylus(
            {
                use: [stylus_normalize(), elf_grid(), rupture()],
                compress: comprimir
            })
        )
        .pipe(autoprefixer())
        .pipe(gulp.dest(paths.dest));
});

gulp.task('watch', function() {
    return watch(paths.styles, function() {
        return gulp.start('stylus');
    });
});

gulp.task('default', ['stylus']);
