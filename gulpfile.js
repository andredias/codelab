var gulp = require('gulp');
var stylus = require('gulp-stylus');
var autoprefixer = require('gulp-autoprefixer');
var watch = require('gulp-watch');
var comprimir = true;
var paths = {
    styles: [
        'server/static/styles/styles.styl'
    ],
    dest: 'server/static/css'
};

gulp.task('stylus', function() {
    var stylus_normalize = require('stylus-normalize');
    var elf_grid = require('elf-grid');
    var rupture = require('rupture');
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
    return watch('server/static/styles/*.styl', function() {
        comprimir = false;
        return gulp.start('stylus');
    });
});

gulp.task('default', ['stylus']);
