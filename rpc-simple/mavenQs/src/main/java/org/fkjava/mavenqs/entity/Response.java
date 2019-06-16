package org.fkjava.mavenqs.entity;

import java.util.ArrayList;
import java.util.List;

public class Response {

    private int code;
    private String message;
    private List<String> data;
    private Object datav;

    public Response() {
        this.code = 0;
        this.message = "OK";
        this.data=new ArrayList<String>();
        this.datav=null;
    }

    public int getCode() {
        return code;
    }

    public void setCode(int code) {
        this.code = code;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public Object getData() {
        return data;
    }

    public void setData(String data) {
        this.data.add(data);
    }
    public void setDataV(Object datav) {
        this.datav=datav;
    }
}

