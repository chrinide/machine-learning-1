###
### gunicorn.pp, install package.
###
class package::gunicorn {
    require python

    ## local variables
    $hiera_dev = lookup('development')
    $version   = $hiera_dev['pip']['gunicorn']

    package { 'gunicorn':
        ensure   => $version,
        provider => 'pip',
    }
}