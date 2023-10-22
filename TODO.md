# TODO #

* Memory support
  * Add cleanup function that runs every x days or so.. 
  * There is a small risk that SQLite might lock the python process since python is runnin asynchronosly but SQLite is running single threaded.

* GPU
    * Rotate between different GPUs

* /admin/reload reloads models
    * basic auth for admin

* curl to / responds with config


* Add performance data, how many ms translation took 