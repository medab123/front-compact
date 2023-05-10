<?php

namespace App\Http\Controllers;

use App\Models\History;
use Illuminate\Http\Request;

class HistoryController extends Controller
{
    public function index(){

        $datas = History::all();
        return view("index",compact("datas"));



    }



    public function saveData(Request $request)
    {
        $data = $request->json()->all();
        if (is_array($data) && count($data) > 0 && is_object($data[0] ?? null)) {

            // If data is an array, iterate through each record and save
            $savedData = [];
            foreach ($data as $record) {
                $history = new History();
                $history->start_date = $record["start_date"];
                $history->duration = $record["duration"];
                $history->fp_name = $record["fp_name"];
                $history->save();
                $savedData[] = $history;
            }
            return response()->json($savedData);
        } else {
            // If data is a single record, save and return the saved record
            $history = new History();   
            $history->start_date = $data["start_date"];
            $history->duration = $data["duration"];
            $history->fp_name = $data["fp_name"];
            $history->save();
            return response()->json($history);
        }
    }
    public function resetCounter(Request $request)
    {
        $fp_name = $request->input("fp_name");
        $history = History::where("fp_name", $fp_name)->update(["status" => "inactive"]);
        return  response()->json($history);
    }
}
