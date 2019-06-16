package org.fkjava.mavenqs.entity;
public class Insuser {
    private String display_name;
    private String project_id;
    private String uuid;
    private String float_ip;
    private String ip;
    private String mail;
    private String tap;
    private String name;
    private String rulename;
    private String ruleobject;
    private String ruleinfo;
    private String rulestate;
    private String ruleid;

    private String id;
    private String project_name;
    private String timestamp;
    private String proto;
    private String src_ip;
    private String src_port;
    private String src_mac;
    private String dst_ip;
    private String dst_port;
    private String dst_mac;
    private String type;
    private String info;

    public Insuser(){
    }
    public Insuser(String display_name,String project_id,String uuid,String float_ip,String ip,String mail,String tap,String name,String rulename,String ruleobject,String ruleinfo,String rulestate,String ruleid,
                   String id,String project_name,String timestamp,String proto,String src_ip,String src_port,String src_mac,String dst_ip,String dst_port,String dst_mac,String type,String info) {
        this.display_name=display_name;
        this.project_id=project_id;
        this.uuid=uuid;
        this.float_ip=float_ip;
        this.ip=ip;
        this.mail=mail;
        this.tap=tap;
        this.name=name;
        this.rulename=rulename;
        this.ruleobject=ruleobject;
        this.ruleinfo=ruleinfo;
        this.rulestate=rulestate;
        this.ruleid=ruleid;

        this.id=id;
        this.project_name=project_name;
        this.timestamp=timestamp;
        this.proto=proto;
        this.src_ip=src_ip;
        this.src_port=src_port;
        this.src_mac=src_mac;
        this.dst_ip=dst_ip;
        this.dst_port=dst_port;
        this.dst_mac=dst_mac;
        this.type=type;
        this.info=info;
    }

    public String getDisplayName() {
        return display_name;
    }
    public void setDisplayName(String display_name) {
        this.display_name = display_name;
    }
    public String getProjectId() {
        return project_id;
    }
    public void setProjectId(String project_id) {
        this.project_id = project_id;
    }
    public String getUuid() {
        return uuid;
    }
    public void setUuid(String uuid) {
        this.uuid = uuid;
    }
    public String getFloat_ip() {
        return float_ip;
    }
    public void setFloat_ip(String float_ip) {
        this.float_ip = float_ip;
    }
    public String getIp() {
        return ip;
    }
    public void setIp(String ip) {
        this.ip = ip;
    }
    public String getMail() {
        return mail;
    }
    public void setMail(String mail) {
        this.mail =mail;
    }
    public String getTap() {
        return tap;
    }
    public void setTap(String tap) {
        this.tap = tap;
    }
    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
    public String getRulename() {
        return rulename;
    }
    public void setRulename(String rulename) {
        this.rulename = rulename;
    }
    public String getRuleobject() {
        return ruleobject;
    }
    public void setRuleobject(String ruleobject) {
        this.ruleobject = ruleobject;
    }
    public String getRuleinfo() {
        return ruleinfo;
    }
    public void setRuleinfo(String ruleinfo) {
        this.ruleinfo = ruleinfo;
    }
    public String getRulestate() {
        return rulestate;
    }
    public void setRulestate(String rulestate) {
        this.rulestate = rulestate;
    }
    public String getRuleid() {
        return ruleid;
    }
    public void setRuleid(String ruleid) {
        this.ruleid = ruleid;
    }

    public String getId() { return id; }
    public void setId(String id) {
        this.id = id;
    }
    public String getproject_name() { return project_name; }
    public void setproject_name(String project_name) {
        this.project_name = project_name;
    }
    public String gettimestamp() { return timestamp; }
    public void settimestamp(String timestamp) {
        this.timestamp = timestamp;
    }
    public String getproto() { return proto; }
    public void setproto(String proto) {
        this.proto = proto;
    }
    public String getsrc_ip() { return src_ip; }
    public void setsrc_ip(String src_ip) {
        this.src_ip = src_ip;
    }
    public String getsrc_port() { return src_port; }
    public void setsrc_port(String src_port) {
        this.src_port = src_port;
    }
    public String getsrc_mac() { return src_mac; }
    public void setsrc_mac(String src_mac) {
        this.src_mac = src_mac;
    }
    public String getdst_ip() { return dst_ip; }
    public void setdst_ip(String dst_ip) {
        this.dst_ip = dst_ip;
    }
    public String getdst_port() { return dst_port; }
    public void setdst_port(String dst_port) {
        this.dst_port = dst_port;
    }
    public String getdst_mac() { return dst_mac; }
    public void setdst_mac(String dst_mac) {
        this.dst_mac = dst_mac;
    }
    public String gettype() { return type; }
    public void settype(String type) {
        this.type = type;
    }
    public String getinfo() { return info; }
    public void setinfo(String info) {
        this.info = info;
    }

    public String toProject(){
        return this.project_id;
    }
    public String toVM(){
        return this.display_name+' '+this.uuid+' '+this.float_ip+' '+this.ip;
    }
    public String toName(){
        return this.name;
    }
    public String toRule(){
        return this.rulename+' '+this.ruleobject+' '+this.ruleinfo+' '+this.rulestate+' '+this.ruleid;
    }
    public String toPast(String pastshow){
        if(pastshow.equals("display_name")) return this.display_name;
        else if(pastshow.equals("id")) return this.id;
        else if(pastshow.equals("timestamp")) return this.timestamp;
        else if(pastshow.equals("project_name")) return this.project_name;
        else if(pastshow.equals("project_id")) return this.project_id;
        else if(pastshow.equals("proto")) return this.proto;
        else if(pastshow.equals("src_ip")) return this.src_ip;
        else if(pastshow.equals("src_port")) return this.src_port;
        else if(pastshow.equals("src_mac")) return this.src_mac;
        else if(pastshow.equals("dst_ip")) return this.dst_ip;
        else if(pastshow.equals("dst_port")) return this.dst_port;
        else if(pastshow.equals("dst_mac")) return this.dst_mac;
        else if(pastshow.equals("type")) return this.type;
        else if(pastshow.equals("info")) return this.info;
        else return this.display_name+" "+this.id+" "+this.timestamp+" "+this.project_name+" "+this.project_id+" "+this.proto+" "+this.src_ip+" "+this.src_port+" "+this.src_mac+" "+this.dst_ip+" "+this.dst_port+" "+this.dst_mac+" "+this.type+" "+this.info;
    }
    public String toPastAll(){
        return this.display_name+" "+this.id+" "+this.timestamp+" "+this.project_name+" "+this.project_id+" "+this.proto+" "+this.src_ip+" "+this.src_port+" "+this.src_mac+" "+this.dst_ip+" "+this.dst_port+" "+this.dst_mac+" "+this.type+" "+this.info;
    }
}

