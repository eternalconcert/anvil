var argv = require('minimist')(process.argv.slice(2));
var fs = require('fs')
var less = require('less')

var SOURCE_DIR = argv['s']
var BUILD_DIR = argv['o'] + 'styles/'

function log(message) {
    console.log("[INFO] Less renderer: " + message);
}

function log_error(message) {
    console.log("[ERROR] Less renderer: " + message);
}

fs.readdir(SOURCE_DIR, function(errors, filenames) {
        log('Found less files: ' + filenames);
        filenames.forEach(function(filename) {
            render_style(filename);
            }
        )
    }
)

function render_style(filename) {
    fs.readFile(SOURCE_DIR + filename, function(error, data) {
            if (error) {
                log(error);
            }
            var less_data = data.toString();
            log('Rendering CSS file: ' + filename);

            less.render(less_data, function(error, output) {
                if (error) {
                        log_error(error);
                    }
                else {
                        fs.writeFile(BUILD_DIR + filename.replace('less', 'css'), output.css, () => {});
                    }
                }
            )
        }
    )
}
