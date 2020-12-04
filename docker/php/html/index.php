<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <title>Youtube Channel Statistics</title>
    <link rel="stylesheet" type="text/css" href="index.css">
    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery.tablesorter/2.31.0/js/jquery.tablesorter.min.js"></script>
    <script>
        // 先頭2行はソート対象外
        $(document).ready(function() {
            $('#fav-table').tablesorter({
                headers: {
                    0: {sorter: false},
                    1: {sorter: false}
                }
            });
        });
    </script>
<body>

    <header>
        <p align="center"><img src="img/header_icon.png"></p>
    </header>

    <dev>
        <?php
            $record_set = null;

            try {
                $dbh = new PDO('mysql:host=mysql_db;dbname=youtube;charset=utf8;', 'user', 'password');
                $sql = " SELECT "
                	   . "   ch.name, "
                     . "   ch.thumbnail_s, "
                     . "   DATE_FORMAT(ch.published_date, '%Y/%m/%d') published_date, "
                     . "   st.subscriber, "
                     . "   st.video_count, "
                     . "   st.view_count "
                     . " FROM "
                	   . "   channel ch, "
                     . "   statistics st "
                     . " WHERE "
                	   . "   ch.channel_id = st.channel_id "
                     . "   AND st.collect_day = (SELECT MAX(collect_day) FROM statistics) "
                     . " ORDER BY "
                     . "   st.subscriber DESC ";

                $record_set = $dbh->query($sql);
                $dbh = null;
            } catch (PDOException $e) {
                echo $e.getMessage();
                exit();
            }
        ?>

        <table id="fav-table">
            <thead>
            <tr>
                <th>サムネイル</th>
                <th>チャンネル名</th>
                <th>登録日</th>
                <th>登録者数</th>
                <th>動画数</th>
                <th>再生数</th>
            </tr>
            </thead>
            <tbody>
                <?php
                    foreach($record_set as $row) {
                        echo "<tr>";
                        echo "<td><img src='" . $row["thumbnail_s"] . "' align='middle'/>" . "</td>";
                        echo "<td>" . $row["name"] . "</td>";
                        echo "<td>" . $row["published_date"] . "</td>";
                        echo "<td>" . $row["subscriber"] . "</td>";
                        echo "<td>" . $row["video_count"] . "</td>";
                        echo "<td>" . $row["view_count"] . "</td>";
                        echo "</tr>";
                    }
                ?>
            </tbody>
        </table>
    </dev>
</body>
</html>
